"""
Module containing the Population grid class object.

Here all the functionality of a Population object is defined.

Useful for the user to understand the functionality,
but copying functionality isn't recommended except if you know what you are doing

Tasks:
    - TODO: add functionality to 'on-init' set arguments
    - TODO: add functionality to return the initial_abundance_hash
    - TODO: add functionality to return the isotope_hash
    - TODO: add functionality to return the isotope_list
    - TODO: add functionality to return the nuclear_mass_hash
    - TODO: add functionality to return the nuclear_mass_list
    - TODO: add functionality to return the source_list
    - TODO: add functionality to return the ensemble_list
    - TODO: consider spreading the functions over more files.
    - TODO: type the private functions
    - TODO: fix the correct object types for the default values of the bse_options
    - TODO: uncomment and implement the HPC functionality
    - TODO: think of a clean and nice way to unload and remove the custom_logging_info library from memory (and from disk)
    - TODO: think of a nice way to remove the loaded grid_code/ generator from memory. 
    - TODO: Create a designated dict for results
"""

import os
import gc
import sys
import copy
import json
import time
import uuid
import logging
import datetime
import argparse
import importlib.util
import multiprocessing
from typing import Union, Any
from collections import (
    OrderedDict,
)
import setproctitle
import py_rinterpolate

from binarycpython.utils.grid_options_defaults import (
    grid_options_defaults_dict,
    moe_di_stefano_default_options,
    _MS_VERBOSITY_LEVEL,
    _CUSTOM_LOGGING_VERBOSITY_LEVEL,
    _LOGGER_VERBOSITY_LEVEL,
)

from binarycpython.utils.custom_logging_functions import (
    autogen_C_logging_code,
    binary_c_log_code,
    create_and_load_logging_function,
)
from binarycpython.utils.functions import (
    get_defaults,
    remove_file,
    filter_arg_dict,
    get_help_all,
    return_binary_c_version_info,
    binaryc_json_serializer,
    verbose_print,
    merge_dicts,
    update_dicts,
    extract_ensemble_json_from_string,
    get_moe_di_stefano_dataset,
    recursive_change_key_to_float,
    custom_sort_dict,
    recursive_change_key_to_string,
    multiply_values_dict,
)


# from binarycpython.utils.hpc_functions import (
#     get_condor_version,
#     get_slurm_version,
#     create_directories_hpc,
#     path_of_calling_script,
#     get_python_details,
# )

from binarycpython.utils.distribution_functions import (
    Moecache,
    LOG_LN_CONVERTER,
    fill_data,
    get_max_multiplicity,
    Arenou2010_binary_fraction,
    raghavan2010_binary_fraction,
    Moe_di_Stefano_2017_multiplicity_fractions,
)

from binarycpython import _binary_c_bindings


class Population:
    """
    Population Object. Contains all the necessary functions to set up, run and process a
    population of systems
    """

    def __init__(self):
        """
        Initialisation function of the population class
        """

        # Different sections of options

        # get binary_c defaults and create a cleaned up dict
        # Setting stuff will check against the defaults to see if the input is correct.
        self.defaults = get_defaults()
        self.cleaned_up_defaults = self._cleanup_defaults()
        self.available_keys = list(self.defaults.keys())
        self.special_params = [
            el for el in list(self.defaults.keys()) if el.endswith("%d")
        ]

        # make the input dictionary
        self.bse_options = {}  # bse_options is just empty.

        # Grid options
        self.grid_options = copy.deepcopy(grid_options_defaults_dict)

        # Custom options
        self.custom_options = {}

        # Load M&s options
        self.grid_options['m&s_options'] = copy.deepcopy(moe_di_stefano_default_options)

        # Write M&S options to a file
        os.makedirs(os.path.join(self.grid_options["tmp_dir"], "moe_distefano"), exist_ok=True)
        with open(os.path.join(os.path.join(self.grid_options["tmp_dir"], "moe_distefano"), "moeopts.dat"), "w") as f:
            f.write(json.dumps(self.grid_options['m&s_options'], indent=4))

        # Argline dict
        self.argline_dict = {}

        # Set main process id
        self.grid_options["_main_pid"] = os.getpid()

        # Set some memory dicts
        self.persistent_data_memory_dict = {}

        #
        self.process_ID = 0

        # Create location to store results. Users should write to this dictionary.
        self.grid_results = {}

        # Create location where ensemble results are written to
        self.grid_ensemble_results = {}

    ###################################################
    # Argument functions
    ###################################################

    # General flow of generating the arguments for the binary_c call:
    # - user provides parameter and value via set (or manually but that is risky)
    # - The parameter names of these input get compared to the parameter names in the self.defaults;
    #    with this, we know that its a valid parameter to give to binary_c.
    # - For a single system, the bse_options will be written as a arg line
    # - For a population the bse_options will get copied to a temp_bse_options dict and updated with
    #   all the parameters generated by the grid

    # I will NOT create the argument line by fully writing ALL the defaults and overriding user
    # input, that seems not necessary because by using the get_defaults() function we already
    # know for sure which parameter names are valid for the binary_c version
    # And because binary_c uses internal defaults, its not necessary to explicitly pass them.
    # I do however suggest everyone to export the binary_c defaults to a file, so that you know
    # exactly which values were the defaults.

    def set(self, **kwargs) -> None:
        """
        Function to set the values of the population. This is the preferred method to set values
        of functions, as it provides checks on the input.

        the bse_options will get populated with all the those that have a key that is present
        in the self.defaults

        the grid_options will get updated with all the those that have a key that is present
        in the self.grid_options

        If neither of above is met; the key and the value get stored in a custom_options dict.

        Args:
            via kwargs all the arguments are either set to binary_c parameters, grid_options or custom_options (see above)
        """

        # Select the params that end with %d

        # Go over all the input
        for key in kwargs:
            # Filter out keys for the bse_options
            if key in self.defaults.keys():
                verbose_print(
                    "adding: {}={} to BSE_options".format(key, kwargs[key]),
                    self.grid_options["verbosity"],
                    1,
                )
                self.bse_options[key] = kwargs[key]

            # Extra check to check if the key fits one of parameter names that end with %d
            elif any(
                [
                    True
                    if (key.startswith(param[:-2]) and len(param[:-2]) < len(key))
                    else False
                    for param in self.special_params
                ]
            ):
                verbose_print(
                    "adding: {}={} to BSE_options by catching the %d".format(
                        key, kwargs[key]
                    ),
                    self.grid_options["verbosity"],
                    1,
                )
                self.bse_options[key] = kwargs[key]

            # Filter out keys for the grid_options
            elif key in self.grid_options.keys():
                verbose_print(
                    "adding: {}={} to grid_options".format(key, kwargs[key]),
                    self.grid_options["verbosity"],
                    1,
                )
                self.grid_options[key] = kwargs[key]

            # The of the keys go into a custom_options dict
            else:
                verbose_print(
                    "<<<< Warning: Key does not match previously known parameter: \
                    adding: {}={} to custom_options >>>>".format(
                        key, kwargs[key]
                    ),
                    self.grid_options["verbosity"],
                    1,
                )
                self.custom_options[key] = kwargs[key]

    def parse_cmdline(self) -> None:
        """
        Function to handle settings values via the command line.
        Best to be called after all the .set(..) lines, and just before the .evolve() is called

        If you input any known parameter (i.e. contained in grid_options, defaults/bse_options
        or custom_options), this function will attempt to convert the input from string
        (because everything is string) to the type of the value that option had before.

        The values of the bse_options are initially all strings, but after user input they
        can change to ints.

        The value of any new parameter (which will go to custom_options) will be a string.

        Tasks:
            - TODO: remove the need for --cmdline
        """

        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--cmdline",
            help='Setting values via the commandline. Input like --cmdline "metallicity=0.02"',
        )
        args = parser.parse_args()

        # How its set up now is that as input you need to give --cmdline "metallicity=0.002"
        # Its checked if this exists and handled accordingly.
        if args.cmdline:
            verbose_print(
                "Found cmdline args. Parsing them now",
                self.grid_options["verbosity"],
                1,
            )

            # Grab the input and split them up, while accepting only non-empty entries
            cmdline_args = args.cmdline
            self.grid_options["_commandline_input"] = cmdline_args
            split_args = [
                cmdline_arg
                for cmdline_arg in cmdline_args.split(" ")
                if not cmdline_arg == ""
            ]

            # Make dict and fill it
            cmdline_dict = {}
            for cmdline_arg in split_args:
                split = cmdline_arg.split("=")
                parameter = split[0]
                value = split[1]
                old_value_found = False

                # Find an old value
                if parameter in self.grid_options:
                    old_value = self.grid_options[parameter]
                    old_value_found = True

                elif parameter in self.defaults:
                    old_value = self.defaults[parameter]
                    old_value_found = True

                elif parameter in self.custom_options:
                    old_value = self.custom_options[parameter]
                    old_value_found = True

                # (attempt to) convert
                if old_value_found:
                    try:
                        verbose_print(
                            "Converting type of {} from {} to {}".format(
                                parameter, type(value), type(old_value)
                            ),
                            self.grid_options["verbosity"],
                            1,
                        )
                        value = type(old_value)(value)
                        verbose_print("Success!", self.grid_options["verbosity"], 1)

                    except ValueError:
                        verbose_print(
                            "Tried to convert the given parameter {}/value {} to its correct type {} (from old value {}). But that wasn't possible.".format(
                                parameter, value, type(old_value), old_value
                            ),
                            self.grid_options["verbosity"],
                            0,
                        )

                # Add to dict
                cmdline_dict[parameter] = value

            # unpack the dictionary into the setting function that handles where the values are set
            self.set(**cmdline_dict)

    def _return_argline(self, parameter_dict=None):
        """
        Function to create the string for the arg line from a parameter dict
        """

        if not parameter_dict:
            parameter_dict = self.bse_options

        argline = "binary_c "

        for param_name in sorted(parameter_dict):
            argline += "{} {} ".format(param_name, parameter_dict[param_name])
        argline = argline.strip()
        return argline

    def _last_grid_variable(self):
        """
        Function that returns the last grid variable
        (i.e. the one with the highest grid_variable_number)
        """

        number = len(self.grid_options["_grid_variables"])
        for grid_variable in self.grid_options["_grid_variables"]:
            if (
                self.grid_options["_grid_variables"][grid_variable][
                    "grid_variable_number"
                ]
                == number - 1
            ):
                return grid_variable

    def add_grid_variable(
        self,
        name: str,
        longname: str,
        valuerange: Union[list, str],
        resolution: str,
        spacingfunc: str,
        probdist: str,
        dphasevol: Union[str, int],
        parameter_name: str,
        gridtype: str = "centred",
        branchpoint: int = 0,
        precode: Union[str, None] = None,
        condition: Union[str, None] = None,
    ) -> None:
        """
        Function to add grid variables to the grid_options.

        The execution of the grid generation will be through a nested for loop.
        Each of the grid variables will get create a deeper for loop.

        The real function that generates the numbers will get written to a new file in the TMP_DIR,
        and then loaded imported and evaluated.
        beware that if you insert some destructive piece of code, it will be executed anyway.
        Use at own risk.

        Tasks:
            - TODO: Fix this complex function.

        Args:
            name:
                name of parameter. This is evaluated as a parameter and you can use it throughout
                the rest of the function

                Examples:
                    name = 'lnm1'
            longname:
                Long name of parameter

                Examples:
                    longname = 'Primary mass'
            range:
                Range of values to take. Does not get used really, the spacingfunction is used to
                get the values from

                Examples:
                    range = [math.log(m_min), math.log(m_max)]
            resolution:
                Resolution of the sampled range (amount of samples).
                TODO: check if this is used anywhere

                Examples:
                    resolution = resolution["M_1"]
            spacingfunction:
                Function determining how the range is sampled. You can either use a real function,
                or a string representation of a function call. Will get written to a file and
                then evaluated.

                Examples:
                    spacingfunction = "const(math.log(m_min), math.log(m_max), {})".format(resolution['M_1'])

            precode:
                Extra room for some code. This code will be evaluated within the loop of the
                sampling function (i.e. a value for lnm1 is chosen already)

                Examples:
                    precode = 'M_1=math.exp(lnm1);'
            probdist:
                Function determining the probability that gets assigned to the sampled parameter

                Examples:
                    probdist = 'Kroupa2001(M_1)*M_1'
            dphasevol:
                part of the parameter space that the total probability is calculated with. Put to -1
                if you want to ignore any dphasevol calculations and set the value to 1
                Examples:
                    dphasevol = 'dlnm1'
            condition:
                condition that has to be met in order for the grid generation to continue
                Examples:
                    condition = 'self.grid_options['binary']==1'
            gridtype:
                Method on how the value range is sampled. Can be either 'edge' (steps starting at
                the lower edge of the value range) or 'centred'
                (steps starting at lower edge + 0.5 * stepsize).
        """

        # TODO: Add check for the grid type input value

        # Add grid_variable
        grid_variable = {
            "name": name,
            "longname": longname,
            "valuerange": valuerange,
            "resolution": resolution,
            "spacingfunc": spacingfunc,
            "precode": precode,
            "probdist": probdist,
            "dphasevol": dphasevol,
            "parameter_name": parameter_name,
            "condition": condition,
            "gridtype": gridtype,
            "branchpoint": branchpoint,
            "grid_variable_number": len(self.grid_options["_grid_variables"]),
        }

        # Check for gridtype input
        if not gridtype in ['edge', 'centred']:
            msg = "Unknown gridtype value. Please start another one"
            raise ValueError(msg)

        # Load it into the grid_options
        self.grid_options["_grid_variables"][grid_variable["name"]] = grid_variable
        verbose_print(
            "Added grid variable: {}".format(json.dumps(grid_variable, indent=4)),
            self.grid_options["verbosity"],
            1,
        )

    ###################################################
    # Return functions
    ###################################################

    def return_population_settings(self) -> dict:
        """
        Function that returns all the options that have been set.

        Can be combined with JSON to make a nice file.

        Returns:
            dictionary containing "bse_options", "grid_options", "custom_options"
        """

        options = {
            "bse_options": self.bse_options,
            "grid_options": self.grid_options,
            "custom_options": self.custom_options,
        }

        return options

    def return_binary_c_version_info(self, parsed=False):
        """
        Function that returns the version information of binary_c
        """

        version_info = return_binary_c_version_info(parsed=parsed)

        return version_info

    def return_binary_c_defaults(self):
        """
        Function that returns the defaults of the binary_c version that is used.
        """

        return self.defaults

    def return_all_info(
        self,
        include_population_settings: bool = True,
        include_binary_c_defaults: bool = True,
        include_binary_c_version_info: bool = True,
        include_binary_c_help_all: bool = True,
    ) -> dict:
        """
        Function that returns all the information about the population and binary_c

        Args:
            include_population_settings:
                whether to include the population_settings (see function return_population_settings)
            include_binary_c_defaults:
                whether to include a dict containing the binary_c parameters and their default
                values
            include_binary_c_version_info:
                whether to include a dict containing all the binary_c version info
                (see return_binary_c_version_info)
            include_binary_c_help_all:
                whether to include a dict containing all the information about
                the binary_c parameters (see get_help_all)

        Return:
            dictionary containing all, or part of, the above dictionaries
        """

        #
        all_info = {}

        #
        if include_population_settings:
            population_settings = self.return_population_settings()
            all_info["population_settings"] = population_settings

        #
        if include_binary_c_defaults:
            binary_c_defaults = self.return_binary_c_defaults()
            all_info["binary_c_defaults"] = binary_c_defaults

        if include_binary_c_version_info:
            binary_c_version_info = return_binary_c_version_info(parsed=True)
            all_info["binary_c_version_info"] = binary_c_version_info

        if include_binary_c_help_all:
            binary_c_help_all_info = get_help_all(print_help=False)
            all_info["binary_c_help_all"] = binary_c_help_all_info

        return all_info

    def export_all_info(
        self,
        use_datadir: bool = True,
        outfile: Union[str, None] = None,
        include_population_settings: bool = True,
        include_binary_c_defaults: bool = True,
        include_binary_c_version_info: bool = True,
        include_binary_c_help_all: bool = True,
    ) -> Union[str, None]:
        """
        Function that exports the all_info to a JSON file

        Tasks:
            - TODO: if any of the values in the dicts here is of a not-serialisable form, then we
                need to change that to a string or something so, use a recursive function that
                goes over the all_info dict and finds those that fit
            - TODO: Fix to write things to the directory. which options do which etc
            - TODO: there's flawed logic here. rewrite this part pls
            - TODO: consider actually just removing the whole 'output to file' part and let the
                user do this.

        Args:
            include_population_settings: whether to include the population_settings
                (see function return_population_settings)
            include_binary_c_defaults: whether to include a dict containing the binary_c parameters
                and their default values
            include_binary_c_version_info: whether to include a dict containing all the binary_c
                version info (see return_binary_c_version_info)
            include_binary_c_help_all: whether to include a dict containing all the information
                about the binary_c parameters (see get_help_all)
            use_datadir: Boolean whether to use the custom_options['data_dir'] to write the file to.
                If the  custom_options["base_filename"] is set, the output file will be called
                <custom_options["base_filename"]>_settings.json. Otherwise a file called
                simulation_<date+time>_settings.json will be created
            outfile: if use_datadir is false, a custom filename will be used
        """

        all_info = self.return_all_info(
            include_population_settings=include_population_settings,
            include_binary_c_defaults=include_binary_c_defaults,
            include_binary_c_version_info=include_binary_c_version_info,
            include_binary_c_help_all=include_binary_c_help_all,
        )

        # Copy dict
        all_info_cleaned = copy.deepcopy(all_info)

        if use_datadir:
            if not self.custom_options.get("base_filename", None):
                base_name = "simulation_{}".format(
                    datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d_%H%M%S")
                )
            else:
                base_name = os.path.splitext(self.custom_options["base_filename"])[0]

            settings_name = base_name + "_settings.json"

            # Check directory, make if necessary
            os.makedirs(self.custom_options["data_dir"], exist_ok=True)

            settings_fullname = os.path.join(
                self.custom_options["data_dir"], settings_name
            )

            verbose_print(
                "Writing settings to {}".format(settings_fullname),
                self.grid_options["verbosity"],
                1,
            )
            # if not outfile.endswith('json'):
            with open(settings_fullname, "w") as file:
                file.write(
                    json.dumps(
                        all_info_cleaned,
                        indent=4,
                        default=binaryc_json_serializer,
                    )
                )
            return settings_fullname
        else:
            verbose_print(
                "Writing settings to {}".format(outfile),
                self.grid_options["verbosity"],
                1,
            )
            if not outfile.endswith("json"):
                verbose_print(
                    "Error: outfile ({}) must end with .json".format(outfile),
                    self.grid_options["verbosity"],
                    0,
                )
                raise ValueError

            with open(outfile, "w") as file:
                file.write(
                    json.dumps(
                        all_info_cleaned, indent=4, default=binaryc_json_serializer
                    )
                )
            return outfile

    def _set_custom_logging(self):
        """
        Function/routine to set all the custom logging so that the function memory pointer
        is known to the grid.
        """

        # C_logging_code gets priority of C_autogen_code
        verbose_print(
            "Creating and loading custom logging functionality",
            self.grid_options["verbosity"],
            1,
        )
        if self.grid_options["C_logging_code"]:
            # Generate entire shared lib code around logging lines
            custom_logging_code = binary_c_log_code(
                self.grid_options["C_logging_code"],
                verbosity=self.grid_options["verbosity"]-(_CUSTOM_LOGGING_VERBOSITY_LEVEL-1),
            )

            # Load memory address
            (
                self.grid_options["custom_logging_func_memaddr"],
                self.grid_options["_custom_logging_shared_library_file"],
            ) = create_and_load_logging_function(
                custom_logging_code,
                verbosity=self.grid_options["verbosity"]-(_CUSTOM_LOGGING_VERBOSITY_LEVEL-1),
                custom_tmp_dir=self.grid_options["tmp_dir"],
            )

        elif self.grid_options["C_auto_logging"]:
            # Generate real logging code
            logging_line = autogen_C_logging_code(
                self.grid_options["C_auto_logging"],
                verbosity=self.grid_options["verbosity"]-(_CUSTOM_LOGGING_VERBOSITY_LEVEL-1),
            )

            # Generate entire shared lib code around logging lines
            custom_logging_code = binary_c_log_code(
                logging_line, verbosity=self.grid_options["verbosity"]-(_CUSTOM_LOGGING_VERBOSITY_LEVEL-1)
            )

            # Load memory address
            (
                self.grid_options["custom_logging_func_memaddr"],
                self.grid_options["_custom_logging_shared_library_file"],
            ) = create_and_load_logging_function(
                custom_logging_code,
                verbosity=self.grid_options["verbosity"]-(_CUSTOM_LOGGING_VERBOSITY_LEVEL-1),
                custom_tmp_dir=self.grid_options["tmp_dir"],
            )

    ###################################################
    # Ensemble functions
    ###################################################

    # Now they are stored in the _process_run_population thing.
    # Needed less code since they all

    ###################################################
    # Evolution functions
    ###################################################

    def _pre_run_cleanup(self):
        """
        Function to clean up some stuff in the grid before a run (like results, ensemble results etc)
        """

        # empty results
        self.grid_options["results"] = {}

    def evolve(self) -> None:
        """
        Entry point function of the whole object. From here, based on the settings,
        we set up a SLURM or CONDOR grid, or if no setting is given we go straight
        to evolving the population

        There are no direct arguments to this function, rather it is based on the grid_options settings:
            grid_options['slurm']: integer Boolean whether to use a slurm_grid evolution
            grid_options['condor']: integer Boolean whether to use a condor_grid evolution

        If neither of the above is set, we continue without using HPC routines
        (that doesn't mean this cannot be run on a server with many cores)

        Returns an dictionary containing the analytics of the run
        TODO: change the way this is done. Slurm & CONDOR should probably do this different
        """

        # Just to make sure we don't have stuff from a previous run hanging around
        self._pre_run_cleanup()

        # Check which type:
        if self.grid_options["slurm"] == 1:
            # Execute Slurm subroutines
            self._slurm_grid()

        elif self.grid_options["condor"] == 1:
            # Execute condor subroutines
            self._condor_grid()
        else:
            # Execute population evolution subroutines
            self._evolve_population()

        # Put all interesting stuff in a variable and output that afterwards, as analytics of the run.
        analytics_dict = {
            "population_name": self.grid_options["_population_id"],
            "evolution_type": self.grid_options["evolution_type"],
            "failed_count": self.grid_options["_failed_count"],
            "failed_prob": self.grid_options["_failed_prob"],
            "failed_systems_error_codes": self.grid_options[
                "_failed_systems_error_codes"
            ].copy(),
            "errors_exceeded": self.grid_options["_errors_exceeded"],
            "errors_found": self.grid_options["_errors_found"],
            "total_probability": self.grid_options["_probtot"],
            "total_count": self.grid_options["_count"],
            "start_timestamp": self.grid_options["_start_time_evolution"],
            "end_timestamp": self.grid_options["_end_time_evolution"],
            "total_mass_run": self.grid_options["_total_mass_run"],
            "total_probability_weighted_mass_run": self.grid_options[
                "_total_probability_weighted_mass_run"
            ],
            "zero_prob_stars_skipped": self.grid_options['_zero_prob_stars_skipped']
        }

        ##
        # Clean up code: remove files, unset values, unload interpolators etc. This is placed in the general evolve function,
        # because that makes for easier control
        self._cleanup()

        return analytics_dict

    def _evolve_population(self):
        """
        Function to evolve populations. This handles the setting up, evolving
        and cleaning up of a population of stars.

        Choices here are:
            to evolve a population via multiprocessing or linearly on 1 core.
            NOT IMPLEMENTED YET to evolve a population via a variable grid, a source file or MC

        Tasks:
            - TODO: include options for different ways of generating a population here. (i.e. MC or source file)
        """

        # Reset some settings: population_id, results, ensemble_results etc
        self.grid_options["_population_id"] = uuid.uuid4().hex

        ##
        # Prepare code/initialise grid.
        # set custom logging, set up store_memaddr, build grid code. dry run grid code.
        self._setup()

        ##
        # Evolve systems: via grid_options one can choose to do this linearly, or
        # multiprocessing method.
        if (
            self.grid_options["evolution_type"]
            in self.grid_options["_evolution_type_options"]
        ):
            if self.grid_options["evolution_type"] == "grid":
                self._evolve_population_grid()
            # elif self.grid_options["evolution_type"] == "mc":
            #     # TODO: add MC option
        else:
            print(
                "Warning. you chose a wrong option for the grid evolution types.\
                Please choose from the following: {}.".format(
                    self.grid_options["_evolution_type_options"]
                )
            )

        #
        self.grid_options["_end_time_evolution"] = time.time()

        # Log and print some information
        verbose_print(
            "Population-{} finished! The total probability was: {}. It took a total of {}s to run {} systems on {} cores".format(
                self.grid_options["_population_id"],
                self.grid_options["_probtot"],
                self.grid_options["_end_time_evolution"]
                - self.grid_options["_start_time_evolution"],
                self.grid_options["_total_starcount"],
                self.grid_options["amt_cores"],
            ),
            self.grid_options["verbosity"],
            0,
        )

        if self.grid_options["_errors_found"]:
            # Some information afterwards
            verbose_print(
                "During the run {} failed systems were found, with a total probability of {} and with the following unique error codes: {} ".format(
                    self.grid_options["_failed_count"],
                    self.grid_options["_failed_prob"],
                    self.grid_options["_failed_systems_error_codes"],
                ),
                self.grid_options["verbosity"],
                0,
            )
            # Some information afterwards
            verbose_print(
                "The full argline commands for {} these systems have been written to {}".format(
                    "ALL"
                    if not self.grid_options["_errors_exceeded"]
                    else "SOME (only the first ones, as there were too many to log all of them)",
                    os.path.join(
                        self.grid_options["tmp_dir"],
                        "failed_systems_{}_X.txt".format(
                            self.grid_options["_population_id"]
                        ),
                    ),
                ),
                self.grid_options["verbosity"],
                0,
            )
        else:
            verbose_print(
                "There were no errors found in this run.",
                self.grid_options["verbosity"],
                0,
            )

    def _get_stream_logger(self, level=logging.DEBUG):
        """Return logger with configured StreamHandler."""
        stream_logger = logging.getLogger("stream_logger")
        stream_logger.handlers = []
        stream_logger.setLevel(level)
        sh = logging.StreamHandler()
        sh.setLevel(level)
        fmt = "[%(asctime)s %(levelname)-8s %(processName)s] --- %(message)s"
        formatter = logging.Formatter(fmt)
        sh.setFormatter(formatter)
        stream_logger.addHandler(sh)

        return stream_logger

    def _system_queue_filler(self, job_queue, amt_cores):
        """
        Function that is responsible for keeping the queue filled.

        This will generate the systems until it is full, and then keeps trying to fill it.
        Will have to play with the size of this.
        """

        stream_logger = self._get_stream_logger()
        if self.grid_options['verbosity'] >= _LOGGER_VERBOSITY_LEVEL:
            stream_logger.debug(f"setting up the system_queue_filler now")

        # Setup of the generator
        self._generate_grid_code(dry_run=False)

        self._load_grid_function()

        generator = self.grid_options["_system_generator"](self, print_results=False)

        # TODO: build in method to handle with the HPC.
        # Continuously fill the queue
        for system_number, system_dict in enumerate(generator):
            # Put job in queue
            job_queue.put((system_number, system_dict))

            # Print some info
            verbose_print(
                "Queue produced system {}".format(system_number),
                self.grid_options["verbosity"],
                2,
            )

            # Print current size
            # print("Current size: {}".format(save_que.qsize()))

            # if system_number%10==0:
            #     print("system_queue_filler: system_number: {}".format(system_number))
            #     bytes_size_Moecache = get_size(Moecache)
            #     print("\tsystem_queue_filler: Size moecache: {}".format(convert_bytes(bytes_size_Moecache)))

            #     bytes_size_distribution_constants = get_size(distribution_constants)
            #     print("\tsystem_queue_filler: Size distribution_constants: {}".format(convert_bytes(bytes_size_distribution_constants)))

            #     bytes_size_self = get_size(dir(self))
            #     print("\tsystem_queue_filler: Size dir(self): {}".format(convert_bytes(bytes_size_self)))

        # Send closing signal to workers. When they receive this they will terminate
        if self.grid_options['verbosity'] >= _LOGGER_VERBOSITY_LEVEL:
            stream_logger.debug(f"Signaling stop to processes")  # DEBUG
    
        for _ in range(amt_cores):
            job_queue.put("STOP")

    def format_ensemble_results(self, ensemble_dictionary):
        """
        Function to handle all the steps of formatting the ensemble output again.

        Input:
            ensemble_dictionary: dictionary containing all the ensemble results
        """

        original_ensemble_results = ensemble_dictionary

        float_format_ensemble_results = recursive_change_key_to_float(original_ensemble_results)
        del original_ensemble_results
        gc.collect()

        # Then sort the dictionary
        sorted_ensemble_results = custom_sort_dict(float_format_ensemble_results)
        del float_format_ensemble_results
        gc.collect()

        # Then Change the keys back to a string but with a %g format.
        reformatted_ensemble_results = recursive_change_key_to_string(sorted_ensemble_results)
        del sorted_ensemble_results
        gc.collect()

        # Put back in the dictionary
        return reformatted_ensemble_results

    def _evolve_population_grid(self):
        """
        Function that handles running the population using multiprocessing.

        First we set up the multiprocessing manager and the job and result queue.

        Then we spawn <self.grid_options["amt_cores"]> amount of process instances,
        and signal them to start.

        While the processes are waiting for their instructions, we start the queue filler,
        which goes over the grid code and puts all the tasks in a queue until its full.

        The processes take these jobs, evolve the and store results.

        When all the systems have been put in the queue we pass a STOP signal
        that will make the processes wrap up.

        We read out the information in the result queue and store them in the grid object
        """

        # Set process name
        setproctitle.setproctitle('binarycpython parent process')
        setproctitle.setthreadtitle("binarycpython parent thread")

        # Set up the manager object that can share info between processes
        manager = multiprocessing.Manager()
        job_queue = manager.Queue(maxsize=self.grid_options["max_queue_size"])
        result_queue = manager.Queue(maxsize=self.grid_options["amt_cores"])

        # Create process instances
        processes = []
        for ID in range(self.grid_options["amt_cores"]):
            processes.append(
                multiprocessing.Process(
                    target=self._process_run_population_grid,
                    args=(job_queue, result_queue, ID),
                )
            )

        # Activate the processes
        for p in processes:
            p.start()

        # Set up the system_queue
        self._system_queue_filler(job_queue, amt_cores=self.grid_options["amt_cores"])

        # Join the processes
        for p in processes:
            p.join()

        # Handle the results by merging all the dictionaries. How that merging happens exactly is
        # described in the merge_dicts description.
        combined_output_dict = OrderedDict()

        sentinel = object()
        for output_dict in iter(result_queue.get, sentinel):
            combined_output_dict = merge_dicts(combined_output_dict, output_dict)
            if result_queue.empty():
                break

        # Extra ensemble result manipulation:
        combined_output_dict['ensemble_results']['ensemble'] = self.format_ensemble_results(combined_output_dict['ensemble_results'].get('ensemble', {}))
        gc.collect()

        # Take into account that we run this on multiple cores
        combined_output_dict["_total_probability_weighted_mass_run"] = combined_output_dict["_total_probability_weighted_mass_run"]

        # Put the values back as object properties
        self.grid_results = combined_output_dict["results"]

        #################################
        # Put Ensemble results
        self.grid_ensemble_results = combined_output_dict[
            "ensemble_results"
        ]  # Ensemble results are also passed as output from that dictionary

        # Add metadata
        self.grid_ensemble_results["metadata"] = {}
        self.grid_ensemble_results["metadata"]["population_id"] = self.grid_options[
            "_population_id"
        ]
        self.grid_ensemble_results["metadata"][
            "total_probability_weighted_mass"
        ] = combined_output_dict["_total_probability_weighted_mass_run"]
        self.grid_ensemble_results["metadata"]["factored_in_probability_weighted_mass"] = False
        if self.grid_options['ensemble_factor_in_probability_weighted_mass']:
            multiply_values_dict(self.grid_ensemble_results['ensemble'], 1/self.grid_ensemble_results["metadata"]['total_probability_weighted_mass'])
            self.grid_ensemble_results["metadata"]["factored_in_probability_weighted_mass"] = True

        # Add settings of the populations
        all_info = self.return_all_info(
            include_population_settings=True,
            include_binary_c_defaults=True,
            include_binary_c_version_info=True,
            include_binary_c_help_all=True,
        )
        self.grid_ensemble_results["metadata"]["settings"] = json.loads(json.dumps(all_info, default=binaryc_json_serializer))

        ##############################
        # Update grid options
        self.grid_options["_failed_count"] = combined_output_dict["_failed_count"]
        self.grid_options["_failed_prob"] = combined_output_dict["_failed_prob"]
        self.grid_options["_failed_systems_error_codes"] = list(
            set(combined_output_dict["_failed_systems_error_codes"])
        )
        self.grid_options["_errors_exceeded"] = combined_output_dict["_errors_exceeded"]
        self.grid_options["_errors_found"] = combined_output_dict["_errors_found"]
        self.grid_options["_probtot"] = combined_output_dict["_probtot"]
        self.grid_options["_count"] = combined_output_dict["_count"]
        self.grid_options["_total_mass_run"] = combined_output_dict["_total_mass_run"]
        self.grid_options[
            "_total_probability_weighted_mass_run"
        ] = combined_output_dict["_total_probability_weighted_mass_run"]
        self.grid_options['_zero_prob_stars_skipped'] = combined_output_dict['_zero_prob_stars_skipped']

    def _evolve_system_mp(self, full_system_dict):
        """
        Function that the multiprocessing evolution method calls to evolve a system

        this function is called by _process_run_population_grid
        """

        binary_cmdline_string = self._return_argline(full_system_dict)

        persistent_data_memaddr = -1
        if self.bse_options.get("ensemble", 0) == 1:
            persistent_data_memaddr = self.persistent_data_memory_dict[self.process_ID]
            # print("thread {}: persistent_data_memaddr: ".format(self.process_ID), persistent_data_memaddr)

        # Get results binary_c
        out = _binary_c_bindings.run_system(
            argstring=binary_cmdline_string,
            custom_logging_func_memaddr=self.grid_options[
                "custom_logging_func_memaddr"
            ],
            store_memaddr=self.grid_options["_store_memaddr"],
            population=1,  # since this system is part of a population, we set this flag to prevent the store from being freed
            persistent_data_memaddr=persistent_data_memaddr,
        )

        # Check for errors
        _ = self._check_binary_c_error(out, full_system_dict)

        # Have some user-defined function do stuff with the data.
        if self.grid_options["parse_function"]:
            self.grid_options["parse_function"](self, out)

    def _process_run_population_grid(self, job_queue, result_queue, ID):
        """
        Worker process that gets items from the job_queue and runs those systems.
        It keeps track of several things like failed systems, total time spent on systems etc.

        Input:
            job_queue: Queue object containing system dicts
            result_queue: Queue where the resulting analytic dictionaries will be put in
            ID: id of the worker process

        """

        # set start timer
        start_process_time = datetime.datetime.now()

        #
        self.process_ID = (
            ID  # Store the ID as a object property again, lets see if that works.
        )

        stream_logger = self._get_stream_logger()
        if self.grid_options['verbosity'] >= _LOGGER_VERBOSITY_LEVEL:
            stream_logger.debug(f"Setting up processor: process-{self.process_ID}")

        # Set the process names
        name = 'binarycpython population thread {}'.format(ID)
        name_proc = 'binarycpython population process {}'.format(ID)
        setproctitle.setproctitle(name_proc)
        setproctitle.setthreadtitle(name)

        # Set to starting up
        with open(
            os.path.join(
                self.grid_options["tmp_dir"],
                "process_status",
                "process_{}.txt".format(self.process_ID),
            ),
            "w",
        ) as f:
            f.write("STARTING")

        # lets try out making stores for all the grids:
        self.grid_options["_store_memaddr"] = _binary_c_bindings.return_store_memaddr()

        verbose_print(
            "Process {} started at {}.\tUsing store memaddr {}".format(
                ID,
                datetime.datetime.now().isoformat(),
                self.grid_options["_store_memaddr"],
            ),
            self.grid_options["verbosity"],
            1,
        )

        # Set the ensemble memory address
        if self.bse_options.get("ensemble", 0) == 1:
            # set persistent data memory address if necessary.
            persistent_data_memaddr = (
                _binary_c_bindings.return_persistent_data_memaddr()
            )

            self.persistent_data_memory_dict = {
                self.process_ID: persistent_data_memaddr
            }

            verbose_print(
                "\tUsing persistent_data memaddr: {}".format(persistent_data_memaddr),
                self.grid_options["verbosity"],
                1,
            )

        # Set up local variables
        localcounter = (
            0  # global counter for the whole loop. (need to be ticked every loop)
        )
        probability_of_systems_run = (
            0  # counter for the probability of the actual systems this tread ran
        )
        number_of_systems_run = (
            0  # counter for the actual amt of systems this thread ran
        )
        zero_prob_stars_skipped = 0

        total_time_calling_binary_c = 0

        total_mass_run = 0
        total_probability_weighted_mass_run = 0

        # Go over the queue
        for system_number, system_dict in iter(job_queue.get, "STOP"):
            if localcounter == 0:

                # Set status to running
                with open(
                    os.path.join(
                        self.grid_options["tmp_dir"],
                        "process_status",
                        "process_{}.txt".format(self.process_ID),
                    ),
                    "w",
                ) as f:
                    f.write("RUNNING")

            # if system_number%10==0:
            #     print("_process_run_population_grid: system_number: {}".format(system_number))
            #     bytes_size_Moecache = get_size(Moecache)
            #     print("\t_process_run_population_grid: Size moecache: {}".format(convert_bytes(bytes_size_Moecache)))

            #     bytes_size_distribution_constants = get_size(distribution_constants)
            #     print("\t_process_run_population_grid: Size distribution_constants: {}".format(convert_bytes(bytes_size_distribution_constants)))

            #     bytes_size_self = get_size(dir(self))
            #     print("\t_process_run_population_grid: Size dir(self): {}".format(convert_bytes(bytes_size_self)))


            # Combine that with the other settings
            full_system_dict = self.bse_options.copy()
            full_system_dict.update(system_dict)

            # In the first system, explicitly check all the keys that are passed to see if
            # they match the keys known to binary_c.
            # Won't do that every system cause that is a bit of a waste of computing time.
            if number_of_systems_run == 0:
                # TODO: Put this someplace else and wrap in a function call
                for key in full_system_dict.keys():
                    if not key in self.available_keys:
                        # Deal with special keys
                        if not any(
                            [
                                True
                                if (
                                    key.startswith(param[:-2])
                                    and len(param[:-2]) < len(key)
                                )
                                else False
                                for param in self.special_params
                            ]
                        ):
                            msg = "Error: Found a parameter unknown to binary_c: {}. Abort".format(
                                key
                            )
                            raise ValueError(msg)

            # self._print_info(
            #     i + 1, self.grid_options["_total_starcount"], full_system_dict
            # )

            #
            verbose_print(
                "Process {} is handling system {}".format(ID, system_number),
                self.grid_options["verbosity"],
                1,
            )

            # In some cases, the whole run crashes. To be able to figure out which system
            # that was on, we log each current system to a file (each thread has one).
            # Each new system overrides the previous
            with open(
                os.path.join(
                    self.grid_options["tmp_dir"],
                    "current_system",
                    "process_{}.txt".format(self.process_ID),
                ),
                "w",
            ) as f:
                binary_cmdline_string = self._return_argline(full_system_dict)
                f.write(binary_cmdline_string)

            start_runtime_binary_c = time.time()

            # If we want to actually evolve the systems
            if self.grid_options["_actually_evolve_system"]:
                run_system = True

                # Check option to ignore 0 probability systems
                if not self.grid_options["run_zero_probability_system"]:
                    if full_system_dict['probability'] == 0:
                        run_system = False
                        zero_prob_stars_skipped += 1

                if run_system:
                    # Evolve the system
                    self._evolve_system_mp(full_system_dict)

            end_runtime_binary_c = time.time()

            total_time_calling_binary_c += (
                end_runtime_binary_c - start_runtime_binary_c
            )  # keep track of total binary_c call time

            # Debug line: logging all the lines
            if self.grid_options["log_runtime_systems"] == 1:
                with open(
                    os.path.join(
                        self.grid_options["tmp_dir"],
                        "runtime_systems",
                        "process_{}.txt".format(self.process_ID),
                    ),
                    "a+",
                ) as f:
                    binary_cmdline_string = self._return_argline(full_system_dict)
                    f.write(
                        "{} {} '{}'\n".format(
                            start_runtime_binary_c,
                            end_runtime_binary_c - start_runtime_binary_c,
                            binary_cmdline_string,
                        )
                    )

            # Keep track of systems:
            probability_of_systems_run += full_system_dict["probability"]
            number_of_systems_run += 1
            localcounter += 1

            # Tally up some numbers
            total_mass_system = (
                full_system_dict.get("M_1", 0)
                + full_system_dict.get("M_2", 0)
                + full_system_dict.get("M_3", 0)
                + full_system_dict.get("M_4", 0)
            )
            total_mass_run += total_mass_system
            total_probability_weighted_mass_run += (
                total_mass_system * full_system_dict["probability"]
            )

        # Set status to finishing
        with open(
            os.path.join(
                self.grid_options["tmp_dir"],
                "process_status",
                "process_{}.txt".format(self.process_ID),
            ),
            "w",
        ) as f:
            f.write("FINISHING")

        if self.grid_options['verbosity'] >= _LOGGER_VERBOSITY_LEVEL:
            stream_logger.debug(f"Process-{self.process_ID} is finishing.")


        # Handle ensemble output: is ensemble==1, then either directly write that data to a file, or combine everything into 1 file.
        ensemble_json = {}  # Make sure it exists already
        if self.bse_options.get("ensemble", 0) == 1:
            verbose_print(
                "Process {}: is freeing ensemble output (using persistent_data memaddr {})".format(
                    ID, self.persistent_data_memory_dict[self.process_ID]
                ),
                self.grid_options["verbosity"],
                2,
            )

            ensemble_raw_output = (
                _binary_c_bindings.free_persistent_data_memaddr_and_return_json_output(
                    self.persistent_data_memory_dict[self.process_ID]
                )
            )
            if ensemble_raw_output is None:
                verbose_print(
                    "Process {}: Warning! Ensemble output is empty. ".format(ID),
                    self.grid_options["verbosity"],
                    1,
                )

            #
            if self.grid_options["combine_ensemble_with_thread_joining"] is True:
                verbose_print(
                    "Process {}: Extracting ensemble info from raw string".format(ID),
                    self.grid_options["verbosity"],
                    2,
                )

                ensemble_json["ensemble"] = extract_ensemble_json_from_string(
                    ensemble_raw_output
                )  # Load this into a dict so that we can combine it later

                # Extra ensemble result manipulation:
                # We need to reformat and multiply by a factor
                ensemble_json["ensemble"] = self.format_ensemble_results(ensemble_json["ensemble"])
                gc.collect()
            else:
                # If we do not allow this, automatically we will export this to the data_dir, in
                # some formatted way
                output_file = os.path.join(
                    self.custom_options["data_dir"],
                    "ensemble_output_{}_{}.json".format(
                        self.grid_options["_population_id"], self.process_ID
                    ),
                )

                # Write to file
                with open(output_file, "w") as f:
                    f.write(ensemble_raw_output)

                print(
                    "Thread {}: Wrote ensemble results directly to file: {}".format(
                        self.process_ID, output_file
                    )
                )

        # free store memory:
        _binary_c_bindings.free_store_memaddr(self.grid_options["_store_memaddr"])

        # Return a set of results and errors
        output_dict = {
            "results": self.grid_results,
            "ensemble_results": ensemble_json,
            "_failed_count": self.grid_options["_failed_count"],
            "_failed_prob": self.grid_options["_failed_prob"],
            "_failed_systems_error_codes": self.grid_options[
                "_failed_systems_error_codes"
            ],
            "_errors_exceeded": self.grid_options["_errors_exceeded"],
            "_errors_found": self.grid_options["_errors_found"],
            "_probtot": probability_of_systems_run,
            "_count": number_of_systems_run,
            "_total_mass_run": total_mass_run,
            "_total_probability_weighted_mass_run": total_probability_weighted_mass_run,
            "_zero_prob_stars_skipped": zero_prob_stars_skipped,
        }

        end_process_time = datetime.datetime.now()

        verbose_print(
            "Process {} finished:\n\tgenerator started at {}, done at {} (total: {}s of which {}s interfacing with binary_c).\n\tRan {} systems with a total probability of {}.\n\tThis thread had {} failing systems with a total probability of {}.\n\tSkipped a total of {} systems because they had 0 probability".format(
                ID,
                start_process_time.isoformat(),
                end_process_time.isoformat(),
                (end_process_time - start_process_time).total_seconds(),
                total_time_calling_binary_c,
                number_of_systems_run,
                probability_of_systems_run,
                self.grid_options["_failed_count"],
                self.grid_options["_failed_prob"],
                zero_prob_stars_skipped,

            ),
            self.grid_options["verbosity"],
            1,
        )

        # Write summary
        summary_dict = {
            "population_id": self.grid_options["_population_id"],
            "process_id": self.process_ID,
            "start_process_time": start_process_time.timestamp(),
            "end_process_time": end_process_time.timestamp(),
            "total_time_calling_binary_c": total_time_calling_binary_c,
            "number_of_systems_run": number_of_systems_run,
            "probability_of_systems_run": probability_of_systems_run,
            "failed_systems": self.grid_options["_failed_count"],
            "failed_probability": self.grid_options["_failed_prob"],
            "failed_system_error_codes": self.grid_options[
                "_failed_systems_error_codes"
            ],
            "zero_prob_stars_skipped": zero_prob_stars_skipped,
        }
        with open(
            os.path.join(
                self.grid_options["tmp_dir"],
                "process_summary",
                "process_{}.json".format(self.process_ID),
            ),
            "w",
        ) as f:
            f.write(json.dumps(summary_dict, indent=4))

        # Set status to running
        with open(
            os.path.join(
                self.grid_options["tmp_dir"],
                "process_status",
                "process_{}.txt".format(self.process_ID),
            ),
            "w",
        ) as f:
            f.write("FINISHED")

        result_queue.put(output_dict)

        if self.grid_options['verbosity'] >= _LOGGER_VERBOSITY_LEVEL:
            stream_logger.debug(f"Process-{self.process_ID} is finished.")

        # Clean up the interpolators if they exist

        # TODO: make a cleanup function for the individual threads
        # TODO: make sure this is necessary. Actually its probably not, because we have a centralised queue

        return

    # Single system
    def evolve_single(self, clean_up_custom_logging_files: bool = True) -> Any:
        """
        Function to run a single system, based on the settings in the grid_options

        The output of the run gets returned, unless a parse function is given to this function.

        Args:
            clean_up_custom_logging_files: whether the clean up all the custom_logging files.

        returns:
            either returns the raw binary_c output, or whatever the parse_function does
        """

        ### Custom logging code:
        self._set_custom_logging()

        # Get argument line
        argline = self._return_argline(self.bse_options)
        verbose_print("Running {}".format(argline), self.grid_options["verbosity"], 1)

        # Run system
        out = _binary_c_bindings.run_system(
            argstring=argline,
            custom_logging_func_memaddr=self.grid_options[
                "custom_logging_func_memaddr"
            ],
            store_memaddr=self.grid_options["_store_memaddr"],
            population=0,
        )

        # TODO: add call to function that cleans up the temp custom logging dir,
        #   and unloads the loaded libraries.
        # TODO: make a switch to turn this off

        if clean_up_custom_logging_files:
            self._clean_up_custom_logging(evol_type="single")

        # Parse
        if self.grid_options["parse_function"]:
            return self.grid_options["parse_function"](self, out)
        return out

    def _setup(self):
        """
        Function to set up the necessary stuff for the population evolution.

        The idea is to do all the stuff that is necessary for a population to run.
        Since we have different methods of running a population, this setup function
        will do different things depending on different settings

        Tasks:
            TODO: Make other kinds of populations possible. i.e, read out type of grid,
                and set up accordingly
            TODO: make this function more general. Have it explicitly set the system_generator
                function
        """

        # Make sure the subdirs of the tmp dir exist:
        os.makedirs(
            os.path.join(self.grid_options["tmp_dir"], "failed_systems"), exist_ok=True
        )
        os.makedirs(
            os.path.join(self.grid_options["tmp_dir"], "current_system"), exist_ok=True
        )
        os.makedirs(
            os.path.join(self.grid_options["tmp_dir"], "process_status"), exist_ok=True
        )
        os.makedirs(
            os.path.join(self.grid_options["tmp_dir"], "process_summary"), exist_ok=True
        )
        os.makedirs(
            os.path.join(self.grid_options["tmp_dir"], "runtime_systems"), exist_ok=True
        )

        # Check for parse function
        if not self.grid_options["parse_function"]:
            print("Warning: No parse function set. Make sure you intended to do this.")

        # #######################
        # ### Custom logging code:
        self._set_custom_logging()

        # ### Load store: Make sure this actually works.

        ### ensemble: make some checks for this
        ## check the settings and set all the warnings.
        if self.bse_options.get("ensemble", None):
            if not self.bse_options.get("ensemble_defer", 0) == 1:
                verbose_print(
                    "Error, if you want to run an ensemble in a population, the output needs to be deferred. Please set 'ensemble_defer' to 1",
                    self.grid_options["verbosity"],
                    0,
                )
                raise ValueError

            if not any(
                [key.startswith("ensemble_filter_") for key in self.bse_options]
            ):
                verbose_print(
                    "Warning: Running the ensemble without any filter requires a lot of available RAM",
                    self.grid_options["verbosity"],
                    0,
                )

            if self.bse_options.get("ensemble_filters_off", 0) != 1:
                verbose_print(
                    "Warning: Running the ensemble without any filter requires a lot of available RAM",
                    self.grid_options["verbosity"],
                    0,
                )

            if self.grid_options["combine_ensemble_with_thread_joining"] == False:
                if not self.custom_options.get("data_dir", None):
                    verbose_print(
                        "Error: chosen to write the ensemble output directly to files but data_dir isn't set",
                        self.grid_options["verbosity"],
                        0,
                    )
                    raise ValueError

        # Check which type of population generation
        if self.grid_options["evolution_type"] == "grid":
            #######################
            # Dry run and getting starcount
            self.grid_options["_probtot"] = 0

            # Put in check
            if len(self.grid_options["_grid_variables"]) == 0:
                print("Error: you haven't defined any grid variables! Aborting")
                raise ValueError

            # Set up the grid code with a dry run option to see total probability
            if self.grid_options['do_dry_run']:
                self._generate_grid_code(dry_run=True)

                # Load the grid code
                self._load_grid_function()

                # Do a dry run
                self._dry_run()

                print(
                    "Total starcount for this run will be: {}".format(
                        self.grid_options["_total_starcount"]
                    )
                )

            #######################
            # Reset values and prepare the grid function
            self.grid_options[
                "_probtot"
            ] = 0  # To make sure that the values are reset. TODO: fix this in a cleaner way
            self.grid_options[
                "_start_time_evolution"
            ] = time.time()  # Setting start time of grid

            # # Making sure the loaded grid code isn't lingering in the main PID
            # self._generate_grid_code(dry_run=False)

            # #
            # self._load_grid_function()

            #
            self.grid_options["_system_generator"] = None

        # Source file
        elif self.grid_options["evolution_type"] == "source_file":
            #######################
            # Dry run and getting starcount
            self.grid_options["_probtot"] = 0

            # Load the grid code
            # TODO: fix this function
            # self._load_source_file_function()

            if self.grid_options['do_dry_run']:
                # Do a dry run
                self._dry_run_source_file()

            print(
                "Total starcount for this run will be: {}".format(
                    self.grid_options["_total_starcount"]
                )
            )

            #######################
            # Reset values and prepare the grid function
            self.grid_options[
                "_probtot"
            ] = 0  # To make sure that the values are reset. TODO: fix this in a cleaner way
            self.grid_options[
                "_start_time_evolution"
            ] = time.time()  # Setting start time of grid

            #
            # TODO: fix this function
            # self._load_source_file_function()
            # self._load_source_file_function(dry_run=False)

            #
            self._load_grid_function()

    def _cleanup(self):
        """
        Function that handles all the cleaning up after the grid has been generated and/or run

        - reset values to 0
        - remove grid file
        - unload grid function/module
        - remove dry grid file
        - unload dry grid function/module
        """

        # Reset values
        self.grid_options["_count"] = 0
        self.grid_options["_probtot"] = 0
        self.grid_options["_system_generator"] = None
        self.grid_options["_failed_count"] = 0
        self.grid_options["_failed_prob"] = 0
        self.grid_options["_errors_found"] = False
        self.grid_options["_errors_exceeded"] = False
        self.grid_options["_failed_systems_error_codes"] = []
        self.grid_options["_total_mass_run"] = 0
        self.grid_options["_total_probability_weighted_mass_run"] = 0

        # Remove files
        # TODO: remove files

        # Unload functions
        # TODO: unload functions

        # Unload/free custom_logging_code
        # TODO: cleanup custom logging code.

        # Also remove the rest of the contents
        keys_moecache = list(Moecache.keys())
        for key in keys_moecache:
            del Moecache[key]

    ###################################################
    # Grid code functions
    #
    # Function below are used to run populations with
    # a variable grid
    ###################################################

    def _generate_grid_code(self, dry_run=False):
        """
        Function that generates the code from which the population will be made.

        dry_run: when True, it will return the starcount at the end so that we know
        what the total amount of systems is.

        The phasevol values are handled by generating a second array

        # TODO: Add correct logging everywhere
        # TODO: add part to handle separation if orbital_period is added. Idea. use default values
        #   for orbital parameters and possibly overwrite those or something.
        # TODO: add centre left right for the spacing.
        # TODO: add sensible description to this function.
        # TODO: Check whether all the probability and phasevol values are correct.
        # TODO: import only the necessary packages/functions
        # TODO: Put all the masses, eccentricities and periods in there already
        # TODO: Put the certain blocks that are repeated in some sub functions
        # TODO: make sure running systems with multiplicity 3+ is also possible.

        Results in a generated file that contains a system_generator function.
        """

        verbose_print("Generating grid code", self.grid_options["verbosity"], 1)

        # Some local values
        code_string = ""
        depth = 0
        indent = "    "
        total_grid_variables = len(self.grid_options["_grid_variables"])

        # Import packages
        code_string += "import math\n"
        code_string += "import numpy as np\n"
        code_string += "from collections import OrderedDict\n"
        code_string += "from binarycpython.utils.distribution_functions import *\n"
        code_string += "from binarycpython.utils.spacing_functions import *\n"
        code_string += "from binarycpython.utils.useful_funcs import *\n"
        code_string += "\n\n"

        # Make the function
        code_string += "def grid_code(self, print_results=True):\n"

        # Increase depth
        depth += 1

        # Write some info in the function
        code_string += (
            indent * depth
            + "# Grid code generated on {}\n".format(
                datetime.datetime.now().isoformat()
            )
            + indent * depth
            + "# This function generates the systems that will be evolved with binary_c\n\n"
        )

        # Set some values in the generated code:
        code_string += indent * depth + "# Setting initial values\n"
        code_string += indent * depth + "_total_starcount = 0\n"
        code_string += indent * depth + "starcounts = [0 for i in range({})]\n".format(
            total_grid_variables
        )
        code_string += indent * depth + "probabilities = {}\n"
        code_string += (
            indent * depth
            + "probabilities_list = [0 for i in range({})]\n".format(
                total_grid_variables
            )
        )
        code_string += (
            indent * depth
            + "probabilities_sum = [0 for i in range({})]\n".format(
                total_grid_variables
            )
        )
        code_string += indent * depth + "parameter_dict = {}\n"
        code_string += indent * depth + "phasevol = 1\n"
        code_string += indent * depth + "\n"

        # Setting up the system parameters
        code_string += indent * depth + "M_1 = None\n"
        code_string += indent * depth + "M_2 = None\n"
        code_string += indent * depth + "M_3 = None\n"
        code_string += indent * depth + "M_4 = None\n"

        code_string += indent * depth + "orbital_period = None\n"
        code_string += indent * depth + "orbital_period_triple = None\n"
        code_string += indent * depth + "orbital_period_quadruple = None\n"

        code_string += indent * depth + "eccentricity = None\n"
        code_string += indent * depth + "eccentricity2 = None\n"
        code_string += indent * depth + "eccentricity3 = None\n"
        code_string += indent * depth + "\n"

        # Prepare the probability
        code_string += indent * depth + "# setting probability lists\n"
        for grid_variable_el in sorted(
            self.grid_options["_grid_variables"].items(),
            key=lambda x: x[1]["grid_variable_number"],
        ):
            # Make probabilities dict
            grid_variable = grid_variable_el[1]
            code_string += indent * depth + 'probabilities["{}"] = 0\n'.format(
                grid_variable["parameter_name"]
            )

        #################################################################################
        # Start of code generation
        #################################################################################
        code_string += indent * depth + "\n"
        # Generate code
        print("Generating grid code")
        for loopnr, grid_variable_el in enumerate(
            sorted(
                self.grid_options["_grid_variables"].items(),
                key=lambda x: x[1]["grid_variable_number"],
            )
        ):
            print("Constructing/adding: {}".format(grid_variable_el[0]))
            grid_variable = grid_variable_el[1]

            #########################
            # Setting up the for loop
            # Add comment for for loop
            code_string += (
                indent * depth
                + "# for loop for {}".format(grid_variable["parameter_name"])
                + "\n"
            )

            code_string += (
                indent * depth
                + "sampled_values_{} = {}".format(
                    grid_variable["name"], grid_variable["spacingfunc"]
                )
                + "\n"
            )

            # TODO: Make clear that the phasevol only works good
            # TODO: add option to ignore this phasevol calculation and set it to 1
            #   if you sample linearly in that thing.
            # if phasevol is <= 0 then we SKIP that whole loop. Its not working then.
            if (
                not grid_variable["dphasevol"] == -1
            ):  # A method to turn off this calculation and allow a phasevol = 1
                code_string += (
                    indent * depth
                    + "phasevol_{} = sampled_values_{}[1]-sampled_values_{}[0]".format(
                        grid_variable["name"],
                        grid_variable["name"],
                        grid_variable["name"],
                    )
                    + "\n"
                )
            else:
                code_string += indent * depth + "phasevol_{} = 1\n".format(
                    grid_variable["name"]
                )

            # # Some print statement
            # code_string += (
            #     indent * depth
            #     + "print('phasevol_{}:', phasevol_{})".format(grid_variable["name"],
            #           grid_variable["name"])
            #     + "\n"
            # )

            # TODO: make sure this works
            # Adding for loop structure
            # code_string += (
            #     indent * depth
            #     + "for {} in sampled_values_{}:".format(
            #         grid_variable["name"], grid_variable["name"]
            #     )
            #     + "\n"
            # )

            code_string += (
                indent * depth
                + "for {}_sample_number in range({}):".format(
                    grid_variable["name"], grid_variable["resolution"]
                )
                + "\n"
            )
            if grid_variable['gridtype'] == 'edge':
                code_string += (
                    indent * (depth+1)
                    + "{} = sampled_values_{}[0] + (sampled_values_{}[1]-sampled_values_{}[0]) * {}_sample_number".format(
                        grid_variable["name"], grid_variable["name"], grid_variable["name"], grid_variable["name"], grid_variable["name"]
                    )
                    + "\n"
                )
            elif grid_variable['gridtype'] == 'centred':
                code_string += (
                    indent * (depth+1)
                    + "{} = sampled_values_{}[0] + 0.5 * (sampled_values_{}[1]-sampled_values_{}[0]) + (sampled_values_{}[1]-sampled_values_{}[0]) * {}_sample_number".format(
                        grid_variable["name"], grid_variable["name"], grid_variable["name"], grid_variable["name"], grid_variable["name"], grid_variable["name"], grid_variable["name"]
                    )
                    + "\n"
                )
            else:
                msg = "Unknown gridtype value. PLease choose a different one"
                raise ValueError(msg)

            #################################################################################
            # Check condition and generate for loop

            # If the grid variable has a condition, write the check and the action
            if grid_variable["condition"]:
                # Add comment
                code_string += (
                    indent * (depth + 1)
                    + "# Condition for {}".format(grid_variable["parameter_name"])
                    + "\n"
                )

                # Add condition check
                code_string += (
                    indent * (depth + 1)
                    + "if not {}:".format(grid_variable["condition"])
                    + "\n"
                )

                # Add condition failed action:
                code_string += (
                    indent * (depth + 2)
                    + 'print("Grid generator: Condition for {} not met!")'.format(
                        grid_variable["parameter_name"]
                    )
                    + "\n"
                )
                code_string += indent * (depth + 2) + "continue" + "\n"

                # Add some white line
                code_string += indent * (depth + 1) + "\n"

            ##############3
            # Add phasevol check:
            code_string += (
                indent * (depth + 1)
                + "if phasevol_{} <= 0:".format(grid_variable["name"])
                + "\n"
            )

            # Add phasevol check action:
            code_string += (
                indent * (depth + 2)
                + 'print("Grid generator: phasevol_{} <= 0!")'.format(
                    grid_variable["name"]
                )
                + "\n"
            )
            code_string += indent * (depth + 2) + "continue" + "\n"

            # Add some white line
            code_string += indent * (depth + 1) + "\n"

            #########################
            # Setting up pre-code and value in some cases
            # Add pre-code
            if grid_variable["precode"]:
                code_string += (
                    indent * (depth + 1)
                    + "{}".format(
                        grid_variable["precode"].replace(
                            "\n", "\n" + indent * (depth + 1)
                        )
                    )
                    + "\n"
                )

            # Set phasevol
            code_string += indent * (depth + 1) + "phasevol *= phasevol_{}\n".format(
                grid_variable["name"],
            )

            #######################
            # Probabilities
            # Calculate probability
            code_string += indent * (depth + 1) + "\n"
            code_string += indent * (depth + 1) + "# Setting probabilities\n"
            code_string += (
                indent * (depth + 1)
                + "d{} = phasevol_{} * ({})".format(
                    grid_variable["name"],
                    grid_variable["name"],
                    grid_variable["probdist"],
                )
                + "\n"
            )

            # Saving probability sum
            code_string += (
                indent * (depth + 1)
                + "probabilities_sum[{}] += d{}".format(
                    grid_variable["grid_variable_number"], grid_variable["name"]
                )
                + "\n"
            )

            if grid_variable["grid_variable_number"] == 0:
                code_string += (
                    indent * (depth + 1)
                    + "probabilities_list[0] = d{}".format(grid_variable["name"])
                    + "\n"
                )
            else:
                code_string += (
                    indent * (depth + 1)
                    + "probabilities_list[{}] = probabilities_list[{}] * d{}".format(
                        grid_variable["grid_variable_number"],
                        grid_variable["grid_variable_number"] - 1,
                        grid_variable["name"],
                    )
                    + "\n"
                )

            #######################
            # Increment starcount for this parameter
            code_string += "\n"
            code_string += indent * (
                depth + 1
            ) + "# Increment starcount for {}\n".format(grid_variable["parameter_name"])

            code_string += (
                indent * (depth + 1)
                + "starcounts[{}] += 1".format(
                    grid_variable["grid_variable_number"],
                )
                + "\n"
            )

            # Add value to dict
            code_string += (
                indent * (depth + 1)
                + 'parameter_dict["{}"] = {}'.format(
                    grid_variable["parameter_name"], grid_variable["parameter_name"]
                )
                + "\n"
            )

            # Add some space
            code_string += "\n"

            # The final parts of the code, where things are returned, are within the deepest loop,
            # but in some cases code from a higher loop needs to go under it again
            # SO I think its better to put an if statement here that checks
            # whether this is the last loop.
            if loopnr == len(self.grid_options["_grid_variables"]) - 1:

                code_string = self._write_gridcode_system_call(
                    code_string,
                    indent,
                    depth,
                    grid_variable,
                    dry_run,
                    grid_variable["branchpoint"],
                )

            # increment depth
            depth += 1

        depth -= 1
        code_string += "\n"

        # Write parts to write below the part that yield the results.
        # this has to go in a reverse order:
        # Here comes the stuff that is put after the deepest nested part that calls returns stuff.
        # Here we will have a
        reverse_sorted_grid_variables = sorted(
            self.grid_options["_grid_variables"].items(),
            key=lambda x: x[1]["grid_variable_number"],
            reverse=True,
        )
        for loopnr, grid_variable_el in enumerate(reverse_sorted_grid_variables):
            grid_variable = grid_variable_el[1]

            code_string += indent * (depth + 1) + "#" * 40 + "\n"
            code_string += (
                indent * (depth + 1)
                + "# Code below is for finalising the handling of this iteration of the parameter {}\n".format(grid_variable["name"])
            )

            # Set phasevol
            # TODO: fix. this isn't supposed to be the value that we give it here. discuss
            code_string += indent * (depth + 1) + "phasevol /= phasevol_{}\n".format(
                grid_variable["name"]
            )
            code_string += indent * (depth + 1) + "\n"

            depth -= 1

            # Check the branchpoint part here. The branchpoint makes sure that we can construct
            # a grid with several multiplicities and still can make the system calls for each
            # multiplicity without reconstructing the grid each time
            if grid_variable["branchpoint"] > 0:

                # Add comment
                code_string += (
                    indent * (depth + 1)
                    + "# Condition for branchpoint at {}".format(
                        reverse_sorted_grid_variables[loopnr + 1][1]["parameter_name"]
                    )
                    + "\n"
                )

                # # Add condition check
                # code_string += (
                #     indent * (depth + 1)
                #     + "if not {}:".format(grid_variable["condition"])
                #     + "\n"
                # )

                # Add branchpoint
                code_string += (
                    indent * (depth + 1)
                    + "if multiplicity=={}:".format(grid_variable["branchpoint"])
                    + "\n"
                )

                code_string = self._write_gridcode_system_call(
                    code_string,
                    indent,
                    depth + 1,
                    reverse_sorted_grid_variables[loopnr + 1][1],
                    dry_run,
                    grid_variable["branchpoint"],
                )
                code_string += "\n"

        ################
        # Finalising print statements
        #
        # code_string += indent * (depth + 1) + "\n"
        code_string += indent * (depth + 1) + "#" * 40 + "\n"
        code_string += indent * (depth + 1) + "if print_results:\n"
        code_string += (
            indent * (depth + 2)
            + "print('Grid has handled {} stars'.format(_total_starcount))\n"
        )
        code_string += (
            indent * (depth + 2)
            + "print('with a total probability of {}'.format(self.grid_options['_probtot']))\n"
        )

        ################
        # Finalising return statement for dry run.
        #
        if dry_run:
            code_string += indent * (depth + 1) + "return _total_starcount\n"

        #################################################################################
        # Stop of code generation. Here the code is saved and written

        # Save the grid code to the grid_options
        verbose_print(
            "Saving grid code to grid_options", self.grid_options["verbosity"], 1
        )

        self.grid_options["code_string"] = code_string

        # Write to file
        gridcode_filename = os.path.join(
            self.grid_options["tmp_dir"],
            "binary_c_grid_{}.py".format(self.grid_options["_population_id"]),
        )
        self.grid_options["gridcode_filename"] = gridcode_filename

        verbose_print(
            "Writing grid code to {}".format(gridcode_filename),
            self.grid_options["verbosity"],
            1,
        )

        with open(gridcode_filename, "w") as file:
            file.write(code_string)


    def _write_gridcode_system_call(
        self, code_string, indent, depth, grid_variable, dry_run, branchpoint
    ):
        #################################################################################
        # Here are the calls to the queuing or other solution. this part is for every system
        # Add comment
        code_string += indent * (depth + 1) + "#" * 40 + "\n"

        if branchpoint:
            code_string += (
                indent * (depth + 1)
                + "# Code below will get evaluated for every system at this level of multiplicity (last one of that being {})\n"
            ).format(grid_variable["name"])
        else:
            code_string += (
                indent * (depth + 1)
                + "# Code below will get evaluated for every generated system\n"
            )

        # Factor in the custom weight input
        code_string += (
            indent * (depth + 1)
            + "\n"
        )
        code_string += (
            indent * (depth + 1)
            + "# Weigh the probability by a custom weighting factor\n"
        )
        code_string += (
            indent * (depth + 1)
            + 'probability = self.grid_options["weight"] * probabilities_list[{}]'.format(
                grid_variable["grid_variable_number"]
            )
            + "\n"
        )

        # Take into account the multiplicity fraction: 
        code_string += (
            indent * (depth + 1)
            + "\n"
        )
        code_string += (
            indent * (depth + 1)
            + "# Factor the multiplicity fraction into the probability\n"
        )
        code_string += (
            indent * (depth + 1)
            + 'probability = probability * self._calculate_multiplicity_fraction(parameter_dict)'
            + "\n"
        )

        # Add division by amount of repeats
        code_string += (
            indent * (depth + 1)
            + "\n"
        )
        code_string += (
            indent * (depth + 1)
            + "# Divide the probability by the amount of repeats\n"
        )

        code_string += (
            indent * (depth + 1)
            + 'probability = probability / self.grid_options["repeat"]'
            + "\n"
        )

        # Now we yield the system self.grid_options["repeat"] times.
        code_string += (
            indent * (depth + 1)
            + "\n"
        )
        code_string += (
            indent * (depth + 1)
            + "# Loop over the repeats\n"
        )
        code_string += (
            indent * (depth + 1) + 'for _ in range(self.grid_options["repeat"]):' + "\n"
        )

        code_string += indent * (depth + 2) + "_total_starcount += 1\n"

        # set probability and phasevol values into the system dict
        code_string += (
            indent * (depth + 2)
            + 'parameter_dict["{}"] = {}'.format("probability", "probability")
            + "\n"
        )
        code_string += (
            indent * (depth + 2)
            + 'parameter_dict["{}"] = {}'.format("phasevol", "phasevol")
            + "\n"
        )

        # Some prints. will be removed
        # code_string += indent * (depth + 1) + "print(probabilities)\n"
        # code_string += (
        #     indent * (depth + 1) + 'print("_total_starcount: ", _total_starcount)\n'
        # )

        # code_string += indent * (depth + 1) + "print(probability)\n"

        # Increment total probability
        code_string += indent * (depth + 2) + "self._increment_probtot(probability)\n"

        if not dry_run:
            # Handling of what is returned, or what is not.
            code_string += indent * (depth + 2) + "yield(parameter_dict)\n"

        # If its a dry run, dont do anything with it
        else:
            code_string += indent * (depth + 2) + "pass\n"

        code_string += indent * (depth + 1) + "#" * 40 + "\n"

        return code_string

    def _load_grid_function(self):
        """
        Function that loads the script containing the grid code.

        TODO: Update this description
        Test function to run grid stuff. mostly to test the import
        """

        # Code to load the
        verbose_print(
            message="Loading grid code function from {}".format(
                self.grid_options["gridcode_filename"]
            ),
            verbosity=self.grid_options["verbosity"],
            minimal_verbosity=1,
        )

        spec = importlib.util.spec_from_file_location(
            "binary_c_python_grid",
            os.path.join(self.grid_options["gridcode_filename"]),
        )
        grid_file = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(grid_file)
        generator = grid_file.grid_code

        self.grid_options["_system_generator"] = generator

        verbose_print("Grid code loaded", self.grid_options["verbosity"], 1)

    def _dry_run(self):
        """
        Function to dry run the grid and know how many stars it will run

        Requires the grid to be built as a dry run grid
        """

        system_generator = self.grid_options["_system_generator"]
        total_starcount = system_generator(self)
        self.grid_options["_total_starcount"] = total_starcount

    def _print_info(self, run_number, total_systems, full_system_dict):
        """
        Function to print info about the current system and the progress of the grid.

        # color info tricks from https://ozzmaker.com/add-colour-to-text-in-python/
        https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python
        """

        # Define frequency
        if self.grid_options["verbosity"] == 1:
            print_freq = 1
        else:
            print_freq = 10

        # Calculate amount of time left

        # calculate amount of time passed
        # time_passed = time.time() - self.grid_options["_start_time_evolution"]

        if run_number % print_freq == 0:
            binary_cmdline_string = self._return_argline(full_system_dict)
            info_string = "{color_part_1} \
            {text_part_1}{end_part_1}{color_part_2} \
            {text_part_2}{end_part_2}".format(
                color_part_1="\033[1;32;41m",
                text_part_1="{}/{}".format(run_number, total_systems),
                end_part_1="\033[0m",
                color_part_2="\033[1;32;42m",
                text_part_2="{}".format(binary_cmdline_string),
                end_part_2="\033[0m",
            )
            print(info_string)

    ###################################################
    # Monte Carlo functions
    #
    # Functions below are used to run populations with
    # Monte Carlo
    ###################################################

    ###################################################
    # Population from file functions
    #
    # Functions below are used to run populations from
    # a file containing binary_c calls
    ###################################################
    def _dry_run_source_file(self):
        """
        Function to go through the source_file and count the amount of lines and the total probability
        """

        system_generator = self.grid_options["_system_generator"]

        total_starcount = 0
        total_probability = 0

        contains_probability = False

        for line in system_generator:
            total_starcount += 1

        total_starcount = system_generator(self)
        self.grid_options["_total_starcount"] = total_starcount

    def _load_source_file(self, check=False):
        """
        Function that loads the source_file that contains a binary_c calls
        """

        if not os.path.isfile(self.grid_options["source_file_filename"]):
            verbose_print("Source file doesnt exist", self.grid_options["verbosity"], 0)

        verbose_print(
            message="Loading source file from {}".format(
                self.grid_options["gridcode_filename"]
            ),
            verbosity=self.grid_options["verbosity"],
            minimal_verbosity=1,
        )

        # We can choose to perform a check on the source file, which checks if the lines start with 'binary_c'
        if check:
            source_file_check_filehandle = open(
                self.grid_options["source_file_filename"], "r"
            )
            for line in source_file_check_filehandle:
                if not line.startswith("binary_c"):
                    failed = True
                    break
            if failed:
                verbose_print(
                    "Error, sourcefile contains lines that do not start with binary_c",
                    self.grid_options["verbosity"],
                    0,
                )
                raise ValueError

        source_file_filehandle = open(self.grid_options["source_file_filename"], "r")

        self.grid_options["_system_generator"] = source_file_filehandle

        verbose_print("Source file loaded", self.grid_options["verbosity"], 1)

    def _dict_from_line_source_file(self, line):
        """
        Function that creates a dict from a binary_c arg line
        """

        if line.startswith("binary_c "):
            line = line.replace("binary_c ", "")

        split_line = line.split()
        arg_dict = {}

        for i in range(0, len(split_line), 2):
            if "." in split_line[i + 1]:
                arg_dict[split_line[i]] = float(split_line[i + 1])
            else:
                arg_dict[split_line[i]] = int(split_line[i + 1])

        return arg_dict

    ###################################################
    # SLURM functions
    #
    # subroutines to run SLURM grids
    ###################################################

    # def _slurm_grid(self):
    #     """
    #     Main function that manages the SLURM setup.

    #     Has three stages:

    #     - setup
    #     - evolve
    #     - join

    #     Which stage is used is determined by the value of grid_options['slurm_command']:

    #     <empty>: the function will know its the user that executed the script and
    #     it will set up the necessary condor stuff

    #     'evolve': evolve_population is called to evolve the population of stars

    #     'join': We will attempt to join the output
    #     """

    #     # Check version
    #     # TODO: Put in function
    #     slurm_version = get_slurm_version()
    #     if not slurm_version:
    #         verbose_print(
    #             "SLURM: Error: No installation of slurm found",
    #             self.grid_options["verbosity"],
    #             0,
    #         )
    #     else:
    #         major_version = int(slurm_version.split(".")[0])
    #         minor_version = int(slurm_version.split(".")[1])

    #         if major_version > 17:
    #             verbose_print(
    #                 "SLURM: Found version {} which is new enough".format(slurm_version),
    #                 self.grid_options["verbosity"],
    #                 1,
    #             )
    #         else:
    #             verbose_print(
    #                 "SLURM: Found version {} which is too old (we require 17+)".format(
    #                     slurm_version
    #                 ),
    #                 self.grid_options["verbosity"],
    #                 0,
    #             )

    #     verbose_print(
    #         "SLURM: Running slurm grid. command={}".format(
    #             self.grid_options["slurm_command"]
    #         ),
    #         self.grid_options["verbosity"],
    #         1,
    #     )

    #     if not self.grid_options["slurm_command"]:
    #         # Setting up
    #         verbose_print(
    #             "SLURM: Main controller script. Setting up",
    #             self.grid_options["verbosity"],
    #             1,
    #         )

    #         # Set up working directories:
    #         verbose_print(
    #             "SLURM: creating working directories", self.grid_options["verbosity"], 1
    #         )
    #         create_directories_hpc(self.grid_options["slurm_dir"])

    #         # Create command
    #         python_details = get_python_details()
    #         scriptname = path_of_calling_script()
    #         command = "{} {}".format(python_details["executable"], scriptname)
    #         command += ' --cmdline "{}"'.format(
    #             " ".join(
    #                 [
    #                     "{}".format(self.grid_options["_commandline_input"]),
    #                     "offset=$jobarrayindex",
    #                     "modulo={}".format(self.grid_options["slurm_njobs"]),
    #                     "vb={}".format(self.grid_options["verbosity"]),
    #                     "slurm_jobid=$jobid",
    #                     "slurm_jobarrayindex=$jobarrayindex",
    #                     "slurm_jobname='binary_grid_'$jobid'.'$jobarrayindex",
    #                     "slurm_njobs={}".format(self.grid_options["slurm_njobs"]),
    #                     "slurm_dir={}".format(self.grid_options["slurm_dir"]),
    #                     "rungrid=1",
    #                     "slurm_command=evolve",
    #                 ]
    #             ).strip()
    #         )

    #         # Construct dict with settings for the script while checking the settings at the same time
    #         # Check settings:
    #         # TODO: check settings
    #         # Create SLURM_DIR script:
    #         slurm_script_options = {}
    #         slurm_script_options["n"] = self.grid_options["slurm_njobs"]
    #         slurm_script_options["njobs"] = self.grid_options["slurm_njobs"]
    #         slurm_script_options["dir"] = self.grid_options["slurm_dir"]
    #         slurm_script_options["memory"] = self.grid_options["slurm_memory"]
    #         slurm_script_options["working_dir"] = self.grid_options[
    #             "slurm_dir"
    #         ]  # TODO: check this
    #         slurm_script_options["command"] = command
    #         # slurm_script_options['streams'] = self.grid_options['streams']

    #         # Construct the script
    #         slurm_script_contents = ""
    #         slurm_script_contents += "#!/bin/bash\n"
    #         slurm_script_contents += "# Slurm file for binary_grid and slurm\n"
    #         slurm_script_contents += "#SBATCH --error={}/stderr/%A.%a\n".format(
    #             self.grid_options["slurm_dir"]
    #         )
    #         slurm_script_contents += "#SBATCH --output={}/stdout/%A.%a\n".format(
    #             self.grid_options["slurm_dir"]
    #         )
    #         slurm_script_contents += "#SBATCH --job-name={}\n".format(
    #             self.grid_options["slurm_jobname"]
    #         )
    #         slurm_script_contents += "#SBATCH --partition={}\n".format(
    #             self.grid_options["slurm_partition"]
    #         )
    #         slurm_script_contents += "#SBATCH --time={}\n".format(
    #             self.grid_options["slurm_time"]
    #         )
    #         slurm_script_contents += "#SBATCH --mem={}\n".format(
    #             self.grid_options["slurm_memory"]
    #         )
    #         slurm_script_contents += "#SBATCH --ntasks={}\n".format(
    #             self.grid_options["slurm_ntasks"]
    #         )
    #         slurm_script_contents += "#SBATCH --array={}\n".format(
    #             self.grid_options["slurm_array"]
    #         )
    #         slurm_script_contents += "\n"

    #         if self.grid_options["slurm_extra_settings"]:
    #             slurm_script_contents += "# Extra settings by user:"
    #             slurm_script_contents += "\n".join(
    #                 [
    #                     "--{}={}".format(
    #                         key, self.grid_options["slurm_extra_settings"][key]
    #                     )
    #                     for key in self.grid_options["slurm_extra_settings"]
    #                 ]
    #             )

    #         slurm_script_contents += '# set status to "running"\n'
    #         slurm_script_contents += (
    #             'echo "running" > {}/status/$jobid.$jobarrayindex\n\n'.format(
    #                 self.grid_options["slurm_dir"]
    #             )
    #         )
    #         slurm_script_contents += "# run grid of stars\n"
    #         slurm_script_contents += "{}\n\n".format(command)
    #         slurm_script_contents += '# set status to "finished"\n'
    #         slurm_script_contents += (
    #             'echo "finished" > {}/status/$jobid.$jobarrayindex\n'.format(
    #                 self.grid_options["slurm_dir"]
    #             )
    #         )
    #         slurm_script_contents += "\n"

    #         if self.grid_options["slurm_postpone_join"]:
    #             slurm_script_contents += "{} rungrid=0 results_hash_dumpfile={}/results/$jobid.all slurm_command=join\n".format(
    #                 command, self.grid_options["slurm_dir"]
    #             )

    #         # Write script to file
    #         slurm_script_filename = os.path.join(
    #             self.grid_options["slurm_dir"], "slurm_script"
    #         )
    #         with open(slurm_script_filename, "w") as slurm_script_file:
    #             slurm_script_file.write(slurm_script_contents)

    #         # Execute or postpone
    #         if self.grid_options["slurm_postpone_sbatch"]:
    #             # Execute or postpone the real call to sbatch
    #             sbatch_command = "sbatch {}".format(slurm_script_filename)
    #             verbose_print(
    #                 "running slurm script {}".format(slurm_script_filename),
    #                 self.grid_options["verbosity"],
    #                 0,
    #             )
    #             # subprocess.Popen(sbatch_command, close_fds=True)
    #             # subprocess.Popen(sbatch_command, creationflags=subprocess.DETACHED_PROCESS)
    #             verbose_print("Submitted scripts.", self.grid_options["verbosity"], 0)
    #         else:
    #             verbose_print(
    #                 "Slurm script is in {} but hasnt been executed".format(
    #                     slurm_script_filename
    #                 ),
    #                 self.grid_options["verbosity"],
    #                 0,
    #             )

    #         verbose_print("all done!", self.grid_options["verbosity"], 0)
    #         exit()

    #     elif self.grid_options["slurm_command"] == "evolve":
    #         # Part to evolve the population.
    #         # TODO: decide how many CPUs
    #         verbose_print(
    #             "SLURM: Evolving population", self.grid_options["verbosity"], 1
    #         )

    #         #
    #         self.evolve_population()

    #     elif self.grid_options["slurm_command"] == "join":
    #         # Joining the output.
    #         verbose_print("SLURM: Joining results", self.grid_options["verbosity"], 1)

    ###################################################
    # CONDOR functions
    #
    # subroutines to run CONDOR grids
    ###################################################

    #     def _condor_grid(self):
    #         """
    #         Main function that manages the CONDOR setup.

    #         Has three stages:

    #         - setup
    #         - evolve
    #         - join

    #         Which stage is used is determined by the value of grid_options['condor_command']:

    #         <empty>: the function will know its the user that executed the script and
    #         it will set up the necessary condor stuff

    #         'evolve': evolve_population is called to evolve the population of stars

    #         'join': We will attempt to join the output
    #         """

    #         # TODO: Put in function
    #         condor_version = get_condor_version()
    #         if not condor_version:
    #             verbose_print(
    #                 "CONDOR: Error: No installation of condor found",
    #                 self.grid_options["verbosity"],
    #                 0,
    #             )
    #         else:
    #             major_version = int(condor_version.split(".")[0])
    #             minor_version = int(condor_version.split(".")[1])

    #             if (major_version == 8) and (minor_version > 4):
    #                 verbose_print(
    #                     "CONDOR: Found version {} which is new enough".format(
    #                         condor_version
    #                     ),
    #                     self.grid_options["verbosity"],
    #                     0,
    #                 )
    #             elif major_version > 9:
    #                 verbose_print(
    #                     "CONDOR: Found version {} which is new enough".format(
    #                         condor_version
    #                     ),
    #                     self.grid_options["verbosity"],
    #                     0,
    #                 )
    #             else:
    #                 verbose_print(
    #                     "CONDOR: Found version {} which is too old (we require 8.3/8.4+)".format(
    #                         condor_version
    #                     ),
    #                     self.grid_options["verbosity"],
    #                     0,
    #                 )

    #         verbose_print(
    #             "Running Condor grid. command={}".format(
    #                 self.grid_options["condor_command"]
    #             ),
    #             self.grid_options["verbosity"],
    #             1,
    #         )
    #         if not self.grid_options["condor_command"]:
    #             # Setting up
    #             verbose_print(
    #                 "CONDOR: Main controller script. Setting up",
    #                 self.grid_options["verbosity"],
    #                 1,
    #             )

    #             # Set up working directories:
    #             verbose_print(
    #                 "CONDOR: creating working directories",
    #                 self.grid_options["verbosity"],
    #                 1,
    #             )
    #             create_directories_hpc(self.grid_options["condor_dir"])

    #             # Create command
    #             current_workingdir = os.getcwd()
    #             python_details = get_python_details()
    #             scriptname = path_of_calling_script()
    #             # command = "".join([
    #             #     "{}".python_details['executable'],
    #             #     "{}".scriptname,
    #             #     "offset=$jobarrayindex",
    #             #     "modulo={}".format(self.grid_options['condor_njobs']),
    #             #     "vb={}".format(self.grid_options['verbosity'])

    #             #      "results_hash_dumpfile=$self->{_grid_options}{slurm_dir}/results/$jobid.$jobarrayindex",
    #             #      'slurm_jobid='.$jobid,
    #             #      'slurm_jobarrayindex='.$jobarrayindex,
    #             #      'slurm_jobname=binary_grid_'.$jobid.'.'.$jobarrayindex,
    #             #      "slurm_njobs=$njobs",
    #             #      "slurm_dir=$self->{_grid_options}{slurm_dir}",
    #             # );

    #             # Create directory with info for the condor script. By creating this directory we also check whether all the values are set correctly
    #             # TODO: create the condor script.
    #             condor_script_options = {}
    #             # condor_script_options['n'] =
    #             condor_script_options["njobs"] = self.grid_options["condor_njobs"]
    #             condor_script_options["dir"] = self.grid_options["condor_dir"]
    #             condor_script_options["memory"] = self.grid_options["condor_memory"]
    #             condor_script_options["working_dir"] = self.grid_options[
    #                 "condor_working_dir"
    #             ]
    #             condor_script_options["command"] = self.grid_options["command"]
    #             condor_script_options["streams"] = self.grid_options["streams"]

    #             # TODO: condor works with running an executable.

    #             # Create script contents
    #             condor_script_contents = ""
    #             condor_script_contents += """
    # #################################################
    # #
    # # Condor script to run a binary_grid via python
    # #
    # #################################################
    # """
    #             condor_script_contents += "Executable\t= {}".format(executable)
    #             condor_script_contents += "arguments\t= {}".format(arguments)
    #             condor_script_contents += "environment\t= {}".format(environment)
    #             condor_script_contents += "universe\t= {}".format(
    #                 self.grid_options["condor_universe"]
    #             )
    #             condor_script_contents += "\n"
    #             condor_script_contents += "output\t= {}/stdout/$id\n".format(
    #                 self.grid_options["condor_dir"]
    #             )
    #             condor_script_contents += "error\t={}/sterr/$id".format(
    #                 self.grid_options["condor_dir"]
    #             )
    #             condor_script_contents += "log\t={}\n".format(
    #                 self.grid_options["condor_dir"]
    #             )
    #             condor_script_contents += "initialdir\t={}\n".format(current_workingdir)
    #             condor_script_contents += "remote_initialdir\t={}\n".format(
    #                 current_workingdir
    #             )
    #             condor_script_contents += "\n"
    #             condor_script_contents += "steam_output\t={}".format(stream)
    #             condor_script_contents += "steam_error\t={}".format(stream)
    #             condor_script_contents += "+WantCheckpoint = False"
    #             condor_script_contents += "\n"
    #             condor_script_contents += "request_memory\t={}".format(
    #                 self.grid_options["condor_memory"]
    #             )
    #             condor_script_contents += "ImageSize\t={}".format(
    #                 self.grid_options["condor_memory"]
    #             )
    #             condor_script_contents += "\n"

    #             if self.grid_options["condor_extra_settings"]:
    #                 slurm_script_contents += "# Extra settings by user:"
    #                 slurm_script_contents += "\n".join(
    #                     [
    #                         "{}\t={}".format(
    #                             key, self.grid_options["condor_extra_settings"][key]
    #                         )
    #                         for key in self.grid_options["condor_extra_settings"]
    #                     ]
    #                 )

    #             condor_script_contents += "\n"

    #             #   request_memory = $_[0]{memory}
    #             #   ImageSize = $_[0]{memory}

    #             #   Requirements = (1) \&\& (".
    #             #   $self->{_grid_options}{condor_requirements}.")\n";

    #             #
    #             # file name:  my_program.condor
    #             # Condor submit description file for my_program
    #             # Executable      = my_program
    #             # Universe        = vanilla
    #             # Error           = logs/err.$(cluster)
    #             # Output          = logs/out.$(cluster)
    #             # Log             = logs/log.$(cluster)

    #             # should_transfer_files = YES
    #             # when_to_transfer_output = ON_EXIT
    #             # transfer_input_files = files/in1,files/in2

    #             # Arguments       = files/in1 files/in2 files/out1
    #             # Queue

    #             # Write script contents to file
    #             if self.grid_options["condor_postpone_join"]:
    #                 condor_script_contents += "{} rungrid=0 results_hash_dumpfile={}/results/$jobid.all condor_command=join\n".format(
    #                     command, self.grid_options["condor_dir"]
    #                 )

    #             condor_script_filename = os.path.join(
    #                 self.grid_options["condor_dir"], "condor_script"
    #             )
    #             with open(condor_script_filename, "w") as condor_script_file:
    #                 condor_script_file.write(condor_script_contents)

    #             if self.grid_options["condor_postpone_sbatch"]:
    #                 # Execute or postpone the real call to sbatch
    #                 submit_command = "condor_submit {}".format(condor_script_filename)
    #                 verbose_print(
    #                     "running condor script {}".format(condor_script_filename),
    #                     self.grid_options["verbosity"],
    #                     0,
    #                 )
    #                 # subprocess.Popen(sbatch_command, close_fds=True)
    #                 # subprocess.Popen(sbatch_command, creationflags=subprocess.DETACHED_PROCESS)
    #                 verbose_print("Submitted scripts.", self.grid_options["verbosity"], 0)
    #             else:
    #                 verbose_print(
    #                     "Condor script is in {} but hasnt been executed".format(
    #                         condor_script_filename
    #                     ),
    #                     self.grid_options["verbosity"],
    #                     0,
    #                 )

    #             verbose_print("all done!", self.grid_options["verbosity"], 0)
    #             exit()

    #         elif self.grid_options["condor_command"] == "evolve":
    #             # TODO: write this function
    #             # Part to evolve the population.
    #             # TODO: decide how many CPUs
    #             verbose_print(
    #                 "CONDOR: Evolving population", self.grid_options["verbosity"], 1
    #             )

    #             #
    #             self.evolve_population()

    #         elif self.grid_options["condor_command"] == "join":
    #             # TODO: write this function
    #             # Joining the output.
    #             verbose_print("CONDOR: Joining results", self.grid_options["verbosity"], 1)

    #             pass
    ###################################################
    # Unordered functions
    #
    # Functions that arent ordered yet
    ###################################################

    def write_binary_c_calls_to_file(
        self,
        output_dir: Union[str, None] = None,
        output_filename: Union[str, None] = None,
        include_defaults: bool = False,
    ) -> None:
        """
        Function that loops over the grid code and writes the generated parameters to a file.
        In the form of a command line call

        Only useful when you have a variable grid as system_generator. MC wouldn't be that useful

        Also, make sure that in this export there are the basic parameters
        like m1,m2,sep, orb-per, ecc, probability etc.

        On default this will write to the datadir, if it exists

        Tasks:
            - TODO: test this function
            - TODO: make sure the binary_c_python .. output file has a unique name

        Args:
            output_dir: (optional, default = None) directory where to write the file to. If custom_options['data_dir'] is present, then that one will be used first, and then the output_dir
            output_filename: (optional, default = None) filename of the output. If not set it will be called "binary_c_calls.txt"
            include_defaults: (optional, default = None) whether to include the defaults of binary_c in the lines that are written. Beware that this will result in very long lines, and it might be better to just export the binary_c defaults and keep them in a separate file.

        Returns:
            filename: filename that was used to write the calls to
        """

        # Check if there is no compiled grid yet. If not, lets try to build it first.
        if not self.grid_options["_system_generator"]:

            ## check the settings:
            if self.bse_options.get("ensemble", None):
                if self.bse_options["ensemble"] == 1:
                    if not self.bse_options.get("ensemble_defer", 0) == 1:
                        verbose_print(
                            "Error, if you want to run an ensemble in a population, the output needs to be deferred",
                            self.grid_options["verbosity"],
                            0,
                        )
                        raise ValueError

            # Put in check
            if len(self.grid_options["_grid_variables"]) == 0:
                print("Error: you haven't defined any grid variables! Aborting")
                raise ValueError

            #
            self._generate_grid_code(dry_run=False)

            #
            self._load_grid_function()

        # then if the _system_generator is present, we go through it
        if self.grid_options["_system_generator"]:
            # Check if there is an output dir configured
            if self.custom_options.get("data_dir", None):
                binary_c_calls_output_dir = self.custom_options["data_dir"]
            # otherwise check if there's one passed to the function
            else:
                if not output_dir:
                    print(
                        "Error. No data_dir configured and you gave no output_dir. Aborting"
                    )
                    raise ValueError
                binary_c_calls_output_dir = output_dir

            # check if there's a filename passed to the function
            if output_filename:
                binary_c_calls_filename = output_filename
            # otherwise use default value
            else:
                binary_c_calls_filename = "binary_c_calls.txt"

            binary_c_calls_full_filename = os.path.join(
                binary_c_calls_output_dir, binary_c_calls_filename
            )
            print("Writing binary_c calls to {}".format(binary_c_calls_full_filename))

            # Write to file
            with open(binary_c_calls_full_filename, "w") as file:
                # Get defaults and clean them, then overwrite them with the set values.
                if include_defaults:
                    # TODO: make sure that the defaults here are cleaned up properly
                    cleaned_up_defaults = self.cleaned_up_defaults
                    full_system_dict = cleaned_up_defaults.copy()
                    full_system_dict.update(self.bse_options.copy())
                else:
                    full_system_dict = self.bse_options.copy()

                for system in self.grid_options["_system_generator"](self):
                    # update values with current system values
                    full_system_dict.update(system)

                    binary_cmdline_string = self._return_argline(full_system_dict)
                    file.write(binary_cmdline_string + "\n")
        else:
            print("Error. No grid function found!")
            raise ValueError


        return binary_c_calls_full_filename


    def _cleanup_defaults(self):
        """
        Function to clean up the default values:

        from a dictionary, removes the entries that have the following values:
        - "NULL"
        - ""
        - "Function"

        Uses the function from utils.functions

        TODO: Rethink this functionality. seems a bit double, could also be just outside of the class
        """

        binary_c_defaults = self.return_binary_c_defaults().copy()
        cleaned_dict = filter_arg_dict(binary_c_defaults)

        return cleaned_dict

    def _clean_up_custom_logging(self, evol_type):
        """
        Function to clean up the custom logging.
        Has two types:
            'single':
                - removes the compiled shared library
                    (which name is stored in grid_options['_custom_logging_shared_library_file'])
                - TODO: unloads/frees the memory allocated to that shared library
                    (which is stored in grid_options['custom_logging_func_memaddr'])
                - sets both to None
            'multiple':
                - TODO: make this and design this
        """

        if evol_type == "single":
            verbose_print(
                "Cleaning up the custom logging stuff. type: single",
                self.grid_options["verbosity"],
                1,
            )

            # TODO: Unset custom logging code

            # TODO: Unset function memory address
            # print(self.grid_options["custom_logging_func_memaddr"])

            # remove shared library files
            if self.grid_options["_custom_logging_shared_library_file"]:
                remove_file(
                    self.grid_options["_custom_logging_shared_library_file"],
                    self.grid_options["verbosity"],
                )

        if evol_type == "population":
            verbose_print(
                "Cleaning up the custom logging stuffs. type: population",
                self.grid_options["verbosity"],
                1,
            )

            # TODO: make sure that these also work. not fully sure if necessary tho.
            #   whether its a single file, or a dict of files/mem addresses

        if evol_type == "MC":
            pass

    def _increment_probtot(self, prob):
        """
        Function to add to the total probability. For now not used
        """

        self.grid_options["_probtot"] += prob

    def _increment_count(self):
        """
        Function to add to the total amount of stars. For now not used
        """
        self.grid_options["_count"] += 1

    def _set_loggers(self):
        """
        Function to set the loggers for the execution of the grid
        """

        # Set log file
        binary_c_logfile = self.grid_options["log_file"]

        # Create directory
        os.makedirs(os.path.dirname(binary_c_logfile), exist_ok=True)

        # Set up logger
        self.logger = logging.getLogger("binary_c_python_logger")
        self.logger.setLevel(self.grid_options["verbosity"])

        # Reset handlers
        self.logger.handlers = []

        # Set formatting of output
        log_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Make and add file handlers
        # make handler for output to file
        handler_file = logging.FileHandler(filename=os.path.join(binary_c_logfile))
        handler_file.setFormatter(log_formatter)
        handler_file.setLevel(logging.INFO)

        # Make handler for output to stdout
        handler_stdout = logging.StreamHandler(sys.stdout)
        handler_stdout.setFormatter(log_formatter)
        handler_stdout.setLevel(logging.INFO)

        # Add the loggers
        self.logger.addHandler(handler_file)
        self.logger.addHandler(handler_stdout)

    def _check_binary_c_error(self, binary_c_output, system_dict):
        """
        Function to check whether binary_c throws an error and handle accordingly.
        """

        if binary_c_output:
            if (binary_c_output.splitlines()[0].startswith("SYSTEM_ERROR")) or (
                binary_c_output.splitlines()[-1].startswith("SYSTEM_ERROR")
            ):
                verbose_print(
                    "FAILING SYSTEM FOUND",
                    self.grid_options["verbosity"],
                    0,
                )

                # Keep track of the amount of failed systems and their error codes
                self.grid_options["_failed_prob"] += system_dict["probability"]
                self.grid_options["_failed_count"] += 1
                self.grid_options["_errors_found"] = True

                # Try catching the error code and keep track of the unique ones.
                try:
                    error_code = int(
                        binary_c_output.splitlines()[0]
                        .split("with error code")[-1]
                        .split(":")[0]
                        .strip()
                    )

                    if (
                        not error_code
                        in self.grid_options["_failed_systems_error_codes"]
                    ):
                        self.grid_options["_failed_systems_error_codes"].append(
                            error_code
                        )
                except ValueError:
                    verbose_print(
                        "Failed to extract the error-code",
                        self.grid_options["verbosity"],
                        1,
                    )

                # Check if we have exceeded the amount of errors
                if (
                    self.grid_options["_failed_count"]
                    > self.grid_options["failed_systems_threshold"]
                ):
                    if not self.grid_options["_errors_exceeded"]:
                        verbose_print(
                            "Process {} exceeded the maximum ({}) amount of failing systems. Stopped logging them to files now".format(
                                self.process_ID,
                                self.grid_options["failed_systems_threshold"],
                            ),
                            self.grid_options["verbosity"],
                            1,
                        )
                        self.grid_options["_errors_exceeded"] = True

                # If not, write the failing systems to files unique to each process
                else:
                    # Write arg lines to file
                    argstring = self._return_argline(system_dict)
                    with open(
                        os.path.join(
                            self.grid_options["tmp_dir"],
                            "failed_systems",
                            "process_{}.txt".format(self.process_ID),
                        ),
                        "a+",
                    ) as f:
                        f.write(argstring + "\n")
        else:
            verbose_print(
                "binary_c had 0 output. Which is strange. Make sure you mean to do this. If there is actually ensemble output being generated then its fine.",
                self.grid_options["verbosity"],
                2,
            )

    def set_moe_di_stefano_settings(self, options=None):
        """
        Function to set user input configurations for the moe & di Stefano methods
    
        If nothing is passed then we just use the default options
        """

        if options:
            # Take the option dictionary that was given and override.
            options = update_dicts(self.grid_options['m&s_options'], options)
            self.grid_options['m&s_options'] = copy.deepcopy(dict(options))

            # Write options to a file
            os.makedirs(os.path.join(self.grid_options["tmp_dir"], "moe_distefano"), exist_ok=True)
            with open(os.path.join(os.path.join(self.grid_options["tmp_dir"], "moe_distefano"), "moeopts.dat"), "w") as f:
                f.write(json.dumps(self.grid_options['m&s_options'], indent=4))

    def _load_moe_di_stefano_data(self):
        """
        Function to load the moe & di stefano data
        """

        # Only if the grid is loaded and Moecache contains information
        if (not self.grid_options['_loaded_ms_data']) and not Moecache:
            # Load the JSON data
            json_data = get_moe_di_stefano_dataset(self.grid_options['m&s_options'], verbosity=self.grid_options['verbosity'])

            # entry of log10M1 is a list containing 1 dict. We can take the dict out of the list
            json_data["log10M1"] = json_data["log10M1"][0]

            # Get all the masses
            logmasses = sorted(json_data["log10M1"].keys())
            if not logmasses:
                msg = "The table does not contain masses."
                verbose_print(
                    "\tMoe_di_Stefano_2017: {}".format(msg),
                    self.grid_options["verbosity"],
                    0,
                )
                raise ValueError(msg)

            # Write to file
            os.makedirs(os.path.join(self.grid_options["tmp_dir"], "moe_distefano"), exist_ok=True)
            with open(os.path.join(os.path.join(self.grid_options["tmp_dir"], "moe_distefano"), "moe.log"), "w") as logfile:
                logfile.write("log₁₀Masses(M☉) {}\n".format(logmasses))

            # Get all the periods and see if they are all consistently present
            logperiods = []
            for logmass in logmasses:
                if not logperiods:
                    logperiods = sorted(json_data["log10M1"][logmass]["logP"])
                    dlog10P = float(logperiods[1]) - float(logperiods[0])

                current_logperiods = sorted(json_data["log10M1"][logmass]["logP"])

                if not (logperiods == current_logperiods):
                    msg = "Period values are not consistent throughout the dataset"
                    verbose_print(
                        "\tMoe_di_Stefano_2017: {}".format(msg),
                        self.grid_options["verbosity"],
                        0,
                    )
                    raise ValueError(msg)

                ############################################################
                # log10period binwidth : of course this assumes a fixed
                # binwidth, so we check for this too.

                for i in range(len(current_logperiods) - 1):
                    if not dlog10P == (
                        float(current_logperiods[i + 1]) - float(current_logperiods[i])
                    ):
                        msg = "Period spacing is not consistent throughout the dataset"
                        verbose_print(
                            "\tMoe_di_Stefano_2017: {}".format(msg),
                            self.grid_options["verbosity"],
                            0,
                        )
                        raise ValueError(msg)

            # Write to file
            os.makedirs(os.path.join(self.grid_options["tmp_dir"], "moe_distefano"), exist_ok=True)
            with open(
                os.path.join(self.grid_options["tmp_dir"], "moe_distefano", "moe.log"), "a"
            ) as logfile:
                logfile.write("log₁₀Periods(days) {}\n".format(logperiods))

            # Fill the global dict
            for logmass in logmasses:
                # Create the multiplicity table
                if not Moecache.get("multiplicity_table", None):
                    Moecache["multiplicity_table"] = []

                # multiplicity as a function of primary mass
                Moecache["multiplicity_table"].append(
                    [
                        float(logmass),
                        json_data["log10M1"][logmass]["f_multi"],
                        json_data["log10M1"][logmass]["single star fraction"],
                        json_data["log10M1"][logmass]["binary star fraction"],
                        json_data["log10M1"][logmass]["triple/quad star fraction"],
                    ]
                )

                ############################################################
                # a small log10period which we can shift just outside the
                # table to force integration out there to zero
                epslog10P = 1e-8 * dlog10P

                ############################################################
                # loop over either binary or triple-outer periods
                first = 1

                # Go over the periods
                for logperiod in logperiods:
                    # print("logperiod: {}".format(logperiod))
                    ############################################################
                    # distributions of binary and triple star fractions
                    # as a function of mass, period.
                    #
                    # Note: these should be per unit log10P, hence we
                    # divide by $dlog10P

                    if first:
                        first = 0

                        # Create the multiplicity table
                        if not Moecache.get("period_distributions", None):
                            Moecache["period_distributions"] = []

                        ############################################################
                        # lower bound the period distributions to zero probability
                        Moecache["period_distributions"].append(
                            [
                                float(logmass),
                                float(logperiod) - 0.5 * dlog10P - epslog10P,
                                0.0,
                                0.0,
                            ]
                        )
                        Moecache["period_distributions"].append(
                            [
                                float(logmass),
                                float(logperiod) - 0.5 * dlog10P,
                                json_data["log10M1"][logmass]["logP"][logperiod][
                                    "normed_bin_frac_p_dist"
                                ]
                                / dlog10P,
                                json_data["log10M1"][logmass]["logP"][logperiod][
                                    "normed_tripquad_frac_p_dist"
                                ]
                                / dlog10P,
                            ]
                        )
                    Moecache["period_distributions"].append(
                        [
                            float(logmass),
                            float(logperiod),
                            json_data["log10M1"][logmass]["logP"][logperiod][
                                "normed_bin_frac_p_dist"
                            ]
                            / dlog10P,
                            json_data["log10M1"][logmass]["logP"][logperiod][
                                "normed_tripquad_frac_p_dist"
                            ]
                            / dlog10P,
                        ]
                    )

                    ############################################################
                    # distributions as a function of mass, period, q
                    #
                    # First, get a list of the qs given by Moe
                    #
                    qs = sorted(json_data["log10M1"][logmass]["logP"][logperiod]["q"])

                    # Fill the data and 'normalise'
                    qdata = fill_data(
                        qs, json_data["log10M1"][logmass]["logP"][logperiod]["q"]
                    )

                    # Create the multiplicity table
                    if not Moecache.get("q_distributions", None):
                        Moecache["q_distributions"] = []

                    for q in qs:
                        Moecache["q_distributions"].append(
                            [float(logmass), float(logperiod), float(q), qdata[q]]
                        )

                    ############################################################
                    # eccentricity distributions as a function of mass, period, ecc
                    eccs = sorted(json_data["log10M1"][logmass]["logP"][logperiod]["e"])

                    # Fill the data and 'normalise'
                    ecc_data = fill_data(
                        eccs, json_data["log10M1"][logmass]["logP"][logperiod]["e"]
                    )

                    # Create the multiplicity table
                    if not Moecache.get("ecc_distributions", None):
                        Moecache["ecc_distributions"] = []

                    for ecc in eccs:
                        Moecache["ecc_distributions"].append(
                            [float(logmass), float(logperiod), float(ecc), ecc_data[ecc]]
                        )

                ############################################################
                # upper bound the period distributions to zero probability
                Moecache["period_distributions"].append(
                    [
                        float(logmass),
                        float(logperiods[-1]) + 0.5 * dlog10P,  # TODO: why this shift?
                        json_data["log10M1"][logmass]["logP"][logperiods[-1]][
                            "normed_bin_frac_p_dist"
                        ]
                        / dlog10P,
                        json_data["log10M1"][logmass]["logP"][logperiods[-1]][
                            "normed_tripquad_frac_p_dist"
                        ]
                        / dlog10P,
                    ]
                )
                Moecache["period_distributions"].append(
                    [
                        float(logmass),
                        float(logperiods[-1]) + 0.5 * dlog10P + epslog10P,
                        0.0,
                        0.0,
                    ]
                )

            verbose_print(
                "\tMoe_di_Stefano_2017: Length period_distributions table: {}".format(
                    len(Moecache["period_distributions"])
                ),
                self.grid_options["verbosity"],
                _MS_VERBOSITY_LEVEL,
            )
            verbose_print(
                "\tMoe_di_Stefano_2017: Length multiplicity table: {}".format(
                    len(Moecache["multiplicity_table"])
                ),
                self.grid_options["verbosity"],
                _MS_VERBOSITY_LEVEL,
            )
            verbose_print(
                "\tMoe_di_Stefano_2017: Length q table: {}".format(
                    len(Moecache["q_distributions"])
                ),
                self.grid_options["verbosity"],
                _MS_VERBOSITY_LEVEL,
            )
            verbose_print(
                "\tMoe_di_Stefano_2017: Length ecc table: {}".format(
                    len(Moecache["ecc_distributions"])
                ),
                self.grid_options["verbosity"],
                _MS_VERBOSITY_LEVEL,
            )

            # Write to log file
            os.makedirs(os.path.join(self.grid_options["tmp_dir"], "moe_distefano"), exist_ok=True)
            with open(os.path.join(os.path.join(self.grid_options["tmp_dir"], "moe_distefano"), "moecache.json"), "w") as cache_filehandle:
                cache_filehandle.write(json.dumps(Moecache, indent=4))

            # Signal that the data has been loaded
            self.grid_options['_loaded_ms_data'] = True

    def _set_moe_di_stefano_distributions(self):
        """
        Function to set the Moe & di Stefano distribution
        """

        ############################################################
        # first, the multiplicity, this is 1,2,3,4, ...
        # for singles, binaries, triples, quadruples, ...

        max_multiplicity = get_max_multiplicity(self.grid_options['m&s_options']["multiplicity_modulator"])
        verbose_print(
            "\tMoe_di_Stefano_2017: Max multiplicity = {}".format(max_multiplicity),
            self.grid_options["verbosity"],
            _MS_VERBOSITY_LEVEL,
        )
        ######
        # Setting up the grid variables

        # Multiplicity
        self.add_grid_variable(
            name="multiplicity",
            parameter_name="multiplicity",
            longname="multiplicity",
            valuerange=[1, max_multiplicity],
            resolution=4,
            spacingfunc="range(1, 5)",
            precode='self.grid_options["multiplicity"] = multiplicity; self.bse_options["multiplicity"] = multiplicity; options={}'.format(
                self.grid_options['m&s_options']
            ),
            condition="({}[multiplicity-1] > 0)".format(
                str(self.grid_options['m&s_options']["multiplicity_modulator"])
            ),
            gridtype="edge",
            dphasevol=-1,
            probdist=1,
        )

        ############################################################
        # always require M1, for all systems
        #

        # TODO: put in option for the time-adaptive grid.

        # log-spaced m1 with given resolution
        self.add_grid_variable(
            name="lnm1",
            parameter_name="M_1",
            longname="Primary mass",
            resolution="options['resolutions']['M'][0]",
            spacingfunc="const(np.log({}), np.log({}), {})".format(
                self.grid_options['m&s_options']["ranges"]["M"][0],
                self.grid_options['m&s_options']["ranges"]["M"][1],
                self.grid_options['m&s_options']["resolutions"]["M"][0],
            ),
            valuerange=[
                "np.log({})".format(self.grid_options['m&s_options']["ranges"]["M"][0]),
                "np.log({})".format(self.grid_options['m&s_options']["ranges"]["M"][1]),
            ],
            gridtype="centred",
            dphasevol="dlnm1",
            precode='M_1 = np.exp(lnm1); options["M_1"]=M_1',
            probdist="Moe_di_Stefano_2017_pdf({{{}, {}, {}}}, verbosity=self.grid_options['verbosity'])['total_probdens'] if multiplicity == 1 else 1".format(
                str(dict(self.grid_options['m&s_options']))[1:-1], "'multiplicity': multiplicity", "'M_1': M_1"
            ),
        )

        # Go to higher multiplicities
        if max_multiplicity >= 2:
            # binaries: period
            self.add_grid_variable(
                name="log10per",
                parameter_name="orbital_period",
                longname="log10(Orbital_Period)",
                resolution=self.grid_options['m&s_options']["resolutions"]["logP"][0],
                probdist=1.0,
                condition='(self.grid_options["multiplicity"] >= 2)',
                branchpoint=1 if max_multiplicity > 1 else 0, # Signal here to put a branchpoint if we have a max multiplicity higher than 1. 
                gridtype="centred",
                dphasevol="({} * dlog10per)".format(LOG_LN_CONVERTER),
                valuerange=[self.grid_options['m&s_options']["ranges"]["logP"][0], self.grid_options['m&s_options']["ranges"]["logP"][1]],
                spacingfunc="const({}, {}, {})".format(
                    self.grid_options['m&s_options']["ranges"]["logP"][0],
                    self.grid_options['m&s_options']["ranges"]["logP"][1],
                    self.grid_options['m&s_options']["resolutions"]["logP"][0],
                ),
                precode="""orbital_period = 10.0**log10per
qmin={}/M_1
qmax=maximum_mass_ratio_for_RLOF(M_1, orbital_period)
""".format(
                    self.grid_options['m&s_options'].get("Mmin", 0.07)
                ),
            ) # TODO: change the maximum_mass_ratio_for_RLOF 

            # binaries: mass ratio
            self.add_grid_variable(
                name="q",
                parameter_name="M_2",
                longname="Mass ratio",
                valuerange=[
                    self.grid_options['m&s_options']["ranges"]["q"][0]
                    if self.grid_options['m&s_options'].get("ranges", {}).get("q", None)
                    else "options.get('Mmin', 0.07)/M_1",
                    self.grid_options['m&s_options']["ranges"]["q"][1]
                    if self.grid_options['m&s_options'].get("ranges", {}).get("q", None)
                    else "qmax",
                ],
                resolution=self.grid_options['m&s_options']["resolutions"]["M"][1],
                probdist=1,
                gridtype="centred",
                dphasevol="dq",
                precode="""
M_2 = q * M_1
sep = calc_sep_from_period(M_1, M_2, orbital_period)
    """,
                spacingfunc="const({}, {}, {})".format(
                    self.grid_options['m&s_options']["ranges"]["q"][0]
                    if self.grid_options['m&s_options'].get("ranges", {}).get("q", [None, None])[0]
                    else "{}/M_1".format(self.grid_options['m&s_options'].get("Mmin", 0.07)),
                    self.grid_options['m&s_options']["ranges"]["q"][1]
                    if self.grid_options['m&s_options'].get("ranges", {}).get("q", [None, None])[1]
                    else "qmax",
                    self.grid_options['m&s_options']["resolutions"]["M"][1],
                ),
            )

            # (optional) binaries: eccentricity
            if self.grid_options['m&s_options']["resolutions"]["ecc"][0] > 0:
                self.add_grid_variable(
                    name="ecc",
                    parameter_name="eccentricity",
                    longname="Eccentricity",
                    resolution=self.grid_options['m&s_options']["resolutions"]["ecc"][0],
                    probdist=1,
                    gridtype="centred",
                    dphasevol="decc",
                    precode="eccentricity=ecc",
                    valuerange=[
                        self.grid_options['m&s_options']["ranges"]["ecc"][0],  # Just fail if not defined.
                        self.grid_options['m&s_options']["ranges"]["ecc"][1],
                    ],
                    spacingfunc="const({}, {}, {})".format(
                        self.grid_options['m&s_options']["ranges"]["ecc"][0],  # Just fail if not defined.
                        self.grid_options['m&s_options']["ranges"]["ecc"][1],
                        self.grid_options['m&s_options']["resolutions"]["ecc"][0],
                    ),
                )

            # Now for triples and quadruples
            if max_multiplicity >= 3:
                # Triple: period
                self.add_grid_variable(
                    name="log10per2",
                    parameter_name="orbital_period_triple",
                    longname="log10(Orbital_Period2)",
                    resolution=self.grid_options['m&s_options']["resolutions"]["logP"][1],
                    probdist=1.0,
                    condition='(self.grid_options["multiplicity"] >= 3)',
                    branchpoint=2 if max_multiplicity > 2 else 0, # Signal here to put a branchpoint if we have a max multiplicity higher than 1. 
                    gridtype="centred",
                    dphasevol="({} * dlog10per2)".format(LOG_LN_CONVERTER),
                    valuerange=[
                        self.grid_options['m&s_options']["ranges"]["logP"][0],
                        self.grid_options['m&s_options']["ranges"]["logP"][1],
                    ],
                    spacingfunc="const({}, {}, {})".format(
                        self.grid_options['m&s_options']["ranges"]["logP"][0],
                        self.grid_options['m&s_options']["ranges"]["logP"][1],
                        self.grid_options['m&s_options']["resolutions"]["logP"][1],
                    ),
                    precode="""orbital_period_triple = 10.0**log10per2
q2min={}/(M_1+M_2)
q2max=maximum_mass_ratio_for_RLOF(M_1+M_2, orbital_period_triple)
    """.format(
                        self.grid_options['m&s_options'].get("Mmin", 0.07)
                    ),
                )

                # Triples: mass ratio
                # Note, the mass ratio is M_outer/M_inner
                self.add_grid_variable(
                    name="q2",
                    parameter_name="M_3",
                    longname="Mass ratio outer/inner",
                    valuerange=[
                        self.grid_options['m&s_options']["ranges"]["q"][0]
                        if self.grid_options['m&s_options'].get("ranges", {}).get("q", None)
                        else "options.get('Mmin', 0.07)/(M_1+M_2)",
                        self.grid_options['m&s_options']["ranges"]["q"][1]
                        if self.grid_options['m&s_options'].get("ranges", {}).get("q", None)
                        else "q2max",
                    ],
                    resolution=self.grid_options['m&s_options']["resolutions"]["M"][2],
                    probdist=1,
                    gridtype="centred",
                    dphasevol="dq2",
                    precode="""
M_3 = q2 * (M_1 + M_2)
sep2 = calc_sep_from_period((M_1+M_2), M_3, orbital_period_triple)
eccentricity2=0
""",
                    spacingfunc="const({}, {}, {})".format(
                        self.grid_options['m&s_options']["ranges"]["q"][0]
                        if self.grid_options['m&s_options'].get("ranges", {}).get("q", None)
                        else "options.get('Mmin', 0.07)/(M_1+M_2)",
                        self.grid_options['m&s_options']["ranges"]["q"][1]
                        if self.grid_options['m&s_options'].get("ranges", {}).get("q", None)
                        else "q2max",
                        self.grid_options['m&s_options']["resolutions"]["M"][2],
                    ),
                )

                # (optional) triples: eccentricity
                if self.grid_options['m&s_options']["resolutions"]["ecc"][1] > 0:
                    self.add_grid_variable(
                        name="ecc2",
                        parameter_name="eccentricity2",
                        longname="Eccentricity of the triple",
                        resolution=self.grid_options['m&s_options']["resolutions"]["ecc"][1],
                        probdist=1,
                        gridtype="centred",
                        dphasevol="decc2",
                        precode="eccentricity2=ecc2",
                        valuerange=[
                            self.grid_options['m&s_options']["ranges"]["ecc"][0],  # Just fail if not defined.
                            self.grid_options['m&s_options']["ranges"]["ecc"][1],
                        ],
                        spacingfunc="const({}, {}, {})".format(
                            self.grid_options['m&s_options']["ranges"]["ecc"][0],  # Just fail if not defined.
                            self.grid_options['m&s_options']["ranges"]["ecc"][1],
                            self.grid_options['m&s_options']["resolutions"]["ecc"][1],
                        ),
                    )

                if max_multiplicity == 4:
                    # Quadruple: period
                    self.add_grid_variable(
                        name="log10per3",
                        parameter_name="orbital_period_quadruple",
                        longname="log10(Orbital_Period3)",
                        resolution=self.grid_options['m&s_options']["resolutions"]["logP"][2],
                        probdist=1.0,
                        condition='(self.grid_options["multiplicity"] >= 4)',
                        branchpoint=3 if max_multiplicity > 3 else 0, # Signal here to put a branchpoint if we have a max multiplicity higher than 1.
                        gridtype="centred",
                        dphasevol="({} * dlog10per3)".format(LOG_LN_CONVERTER),
                        valuerange=[
                            self.grid_options['m&s_options']["ranges"]["logP"][0],
                            self.grid_options['m&s_options']["ranges"]["logP"][1],
                        ],
                        spacingfunc="const({}, {}, {})".format(
                            self.grid_options['m&s_options']["ranges"]["logP"][0],
                            self.grid_options['m&s_options']["ranges"]["logP"][1],
                            self.grid_options['m&s_options']["resolutions"]["logP"][2],
                        ),
                        precode="""orbital_period_quadruple = 10.0**log10per3
q3min={}/(M_3)
q3max=maximum_mass_ratio_for_RLOF(M_3, orbital_period_quadruple)
    """.format(
                            self.grid_options['m&s_options'].get("Mmin", 0.07)
                        ),
                    )

                    # Quadruple: mass ratio : M_outer / M_inner
                    self.add_grid_variable(
                        name="q3",
                        parameter_name="M_4",
                        longname="Mass ratio outer low/outer high",
                        valuerange=[
                            self.grid_options['m&s_options']["ranges"]["q"][0]
                            if self.grid_options['m&s_options'].get("ranges", {}).get("q", None)
                            else "options.get('Mmin', 0.07)/(M_3)",
                            self.grid_options['m&s_options']["ranges"]["q"][1]
                            if self.grid_options['m&s_options'].get("ranges", {}).get("q", None)
                            else "q3max",
                        ],
                        resolution=self.grid_options['m&s_options']["resolutions"]["M"][3],
                        probdist=1,
                        gridtype="centred",
                        dphasevol="dq3",
                        precode="""
M_4 = q3 * M_3
sep3 = calc_sep_from_period((M_3), M_4, orbital_period_quadruple)
eccentricity3=0
""",
                        spacingfunc="const({}, {}, {})".format(
                            self.grid_options['m&s_options']["ranges"]["q"][0]
                            if self.grid_options['m&s_options'].get("ranges", {}).get("q", None)
                            else "options.get('Mmin', 0.07)/(M_3)",
                            self.grid_options['m&s_options']["ranges"]["q"][1]
                            if self.grid_options['m&s_options'].get("ranges", {}).get("q", None)
                            else "q3max",
                            self.grid_options['m&s_options']["resolutions"]["M"][2],
                        ),
                    )

                    # (optional) triples: eccentricity
                    if self.grid_options['m&s_options']["resolutions"]["ecc"][2] > 0:
                        self.add_grid_variable(
                            name="ecc3",
                            parameter_name="eccentricity3",
                            longname="Eccentricity of the triple+quadruple/outer binary",
                            resolution=self.grid_options['m&s_options']["resolutions"]["ecc"][2],
                            probdist=1,
                            gridtype="centred",
                            dphasevol="decc3",
                            precode="eccentricity3=ecc3",
                            valuerange=[
                                self.grid_options['m&s_options']["ranges"]["ecc"][
                                    0
                                ],  # Just fail if not defined.
                                self.grid_options['m&s_options']["ranges"]["ecc"][1],
                            ],
                            spacingfunc="const({}, {}, {})".format(
                                self.grid_options['m&s_options']["ranges"]["ecc"][
                                    0
                                ],  # Just fail if not defined.
                                self.grid_options['m&s_options']["ranges"]["ecc"][1],
                                self.grid_options['m&s_options']["resolutions"]["ecc"][2],
                            ),
                        )

        # Now we are at the last part.
        # Here we should combine all the information that we calculate and update the options
        # dictionary. This will then be passed to the Moe_di_Stefano_2017_pdf to calculate
        # the real probability. The trick we use is to strip the options_dict as a string
        # and add some keys to it:

        updated_options = "{{{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}}}".format(
            str(dict(self.grid_options['m&s_options']))[1:-1],
            '"multiplicity": multiplicity',
            '"M_1": M_1',
            '"M_2": M_2',
            '"M_3": M_3',
            '"M_4": M_4',
            '"P": orbital_period',
            '"P2": orbital_period_triple',
            '"P3": orbital_period_quadruple',
            '"ecc": eccentricity',
            '"ecc2": eccentricity2',
            '"ecc3": eccentricity3',
        )

        probdist_addition = "Moe_di_Stefano_2017_pdf({}, verbosity=self.grid_options['verbosity'])['total_probdens']".format(
            updated_options
        )

        # and finally the probability calculator
        self.grid_options["_grid_variables"][self._last_grid_variable()][
            "probdist"
        ] = probdist_addition

        verbose_print(
            "\tMoe_di_Stefano_2017: Added final call to the pdf function",
            self.grid_options["verbosity"],
            _MS_VERBOSITY_LEVEL,
        )

        # Signal that the M&S grid has been set
        self.grid_options['_set_ms_grid'] = True

    ################################################################################################
    def Moe_di_Stefano_2017(self, options=None):
        """
        Function to handle setting the user input settings,
        set up the data and load that into interpolators and
        then set the distribution functions

        Takes a dictionary as its only argument
        """

        # Set the user input
        self.set_moe_di_stefano_settings(options=options)

        # Load the data
        self._load_moe_di_stefano_data()

        # construct the grid here
        self._set_moe_di_stefano_distributions()

    def _clean_interpolators(self):
        """
        Function to clean up the interpolators after a run

        We look in the Moecache global variable for items that are interpolators.
        Should be called by the general cleanup function AND the thread cleanup function
        """

        interpolator_keys = []
        for key in Moecache.keys():
            if isinstance(Moecache[key], py_rinterpolate.Rinterpolate):
                interpolator_keys.append(key)

        for key in interpolator_keys:
            Moecache[key].destroy()
            del Moecache[key]
        gc.collect()

    ##### Unsorted functions
    def _calculate_multiplicity_fraction(self, system_dict):
        """
        Function to calculate multiplicity fraction

        Makes use of the self.bse_options['multiplicity'] value. If its not set, it will raise an error

        grid_options['multiplicity_fraction_function'] will be checked for the choice
        """

        # Just return 1 if no option has been chosen
        if self.grid_options['multiplicity_fraction_function'] == 0:
            verbose_print(
                "_calculate_multiplicity_fraction: Chosen not to use any multiplicity fraction.",
                self.grid_options["verbosity"],
                2,
            )

            return 1

        # Raise an error if the multiplicity is not set
        if not system_dict.get('multiplicity', None):
            msg = "Multiplicity value has not been set. When using a specific multiplicity fraction function please set the multiplicity"
            raise ValueError(msg)

        # Go over the chosen options
        if self.grid_options['multiplicity_fraction_function'] == 1:
            # Arenou 2010 will be used
            verbose_print(
                "_calculate_multiplicity_fraction: Using Arenou 2010 to calculate multiplicity fractions",
                self.grid_options["verbosity"],
                2,
            )

            binary_fraction = Arenou2010_binary_fraction(system_dict['M_1'])
            multiplicity_fraction_dict = {1: 1-binary_fraction, 2: binary_fraction, 3: 0, 4: 0}

        elif self.grid_options['multiplicity_fraction_function'] == 2:
            # Raghavan 2010 will be used
            verbose_print(
                "_calculate_multiplicity_fraction: Using Rhagavan 2010 to calculate multiplicity fractions",
                self.grid_options["verbosity"],
                2,
            )

            binary_fraction = raghavan2010_binary_fraction(system_dict['M_1'])
            multiplicity_fraction_dict = {1: 1-binary_fraction, 2: binary_fraction, 3: 0, 4: 0}

        elif self.grid_options['multiplicity_fraction_function'] == 3:
            # We need to check several things now here:

            # First, are the options for the M&S grid set? On start it is filled with the default settings
            if not self.grid_options['m&s_options']:
                msg = "The M&S options do not seem to be set properly. The value is {}".format(self.grid_options['m&s_options'])
                raise ValueError(msg)

            # Second: is the Moecache filled.
            if not Moecache:
                verbose_print(
                    "_calculate_multiplicity_fraction: Moecache is empty. It needs to be filled with the data for the interpolators. Loading the data now",
                    self.grid_options["verbosity"],
                    2,
                )

                # Load the data
                self._load_moe_di_stefano_data()

            # record the prev value
            prev_M1_value_ms = self.grid_options['m&s_options'].get('M_1', None)

            # Set value of M1 of the current system
            self.grid_options['m&s_options']['M_1'] = system_dict['M_1']

            # Calculate the multiplicity fraction
            multiplicity_fraction_list = Moe_di_Stefano_2017_multiplicity_fractions(self.grid_options['m&s_options'], self.grid_options["verbosity"])

            # Turn into dict
            multiplicity_fraction_dict = {el+1:multiplicity_fraction_list[el] for el in range(len(multiplicity_fraction_list))}

            # Set the prev value back
            self.grid_options['m&s_options']['M_1'] = prev_M1_value_ms

        # we don't know what to do next
        else:
            msg = "Chosen value for the multiplicity fraction function is not known."
            raise ValueError(msg)

        verbose_print(
            "Multiplicity: {} multiplicity_fraction: {}".format(system_dict['multiplicity'], multiplicity_fraction_dict[system_dict['multiplicity']]),
            self.grid_options["verbosity"],
            2,
        )

        return multiplicity_fraction_dict[system_dict['multiplicity']]
