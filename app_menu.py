"""
~~~~~~~~~~~~~~~~~~~~~~
This module provides CliMenu class to manage cli visual layer of the application
"""
import logging

VER = "1.0"
IND = "                "

OPTION_1 = "Check detailed forecast for particular location"
OPTION_2 = "Check temperature forecast with historical data"
OPTION_3 = "Check weather forecast for your trip"
OPTION_EXIT = "Exit"


class CliMenu:
    """Class CliMenu - set of method to print menu and visual layer"""

    MENU = {
        1: OPTION_1,
        2: OPTION_2,
        3: OPTION_3,
        4: OPTION_EXIT,
    }

    @staticmethod
    def print_banner():
        """Static method to print app baner with name and version"""
        logging.info(
            f"""\n
                **********************************************************************************
                *                                                                                *
                *                     Weather Forecast Tool ver. {VER}                             *
                *                                                                                *   
                **********************************************************************************\n"""
        )

    @staticmethod
    def print_logo():
        """Static method to print logo in ASCI"""
        logging.info(
            """\n
                **********************************************************************************                                                                   
                *             %     %%.    .%                                                    *    
                *             %%%   %%.   %%                                                     *    
                *        %,     %.       %%     #%                                               *    
                *         .%%%  %%%%   %%%#  %%%     %%%%%%%%%%,                                 *    
                *             *%%         %%     %%%%           %%%                              *    
                *      %%%%%% %%               %%%                 %%                            *    
                *             *%%     %%%%%%%%%%                    #%#                          *    
                *          %%%     %%%                               %%                          *    
                *        %*      %%                                  %%%%%#                      *    
                *            #%%%%                                         %%%                   *    
                *       (%%%                                                  %%                 *    
                *     *%%                                                      %%                *    
                *    .%#                                                        %%               *    
                *    %%                                                        %%(               *    
                *     %%                                                       %%                *    
                *      %%                                                    %%,                 *    
                *        %%%%                                           .%%%%                    *    
                *             ,///////////////////////////////////////*                          *    
                *                                                                                *
                **********************************************************************************  \n"""
        )

    @staticmethod
    def print_options():
        """Static method to print main menu"""
        for key, item in CliMenu.MENU.items():
            logging.info(f"{IND}{key} ---------> {item}")

    @staticmethod
    def choose_option() -> int:
        """Static method to check which menu option was selected

        Returns:
            int: number of selected option
        """
        try:
            option = int(input(f"{IND}Enter your choice: "))
            logging.info("")
            return int(option)
        except ValueError:
            logging.info("Error: Wrong input. please enter a number ...\n")
            return -1

    @staticmethod
    def check_if_key_pressed():
        """Static method to provide check if key "q" or "r" is pressed
        'r' - to proceed the execution
        'q' - to abort the execution
        """
        while True:
            pressed_key = input(
                '-----> Type "r" to RUN or "q" to ABORT and press ENTER: '
            )
            logging.info("")
            if pressed_key.lower() == "q":
                logging.info("Info: You pressed 'q' - to abort the execution \n")
                return False

            if pressed_key.lower() == "r":
                logging.info("Info: You pressed 'r' -  to proceed the execution \n")
                return True
            logging.info("Info: Wrong key, please try again \n")

    @staticmethod
    def check_if_key_pressed_yes_no():
        """Static method to provide check if key "q" or "r" is pressed
        'r' - to proceed the execution
        'q' - to abort the execution
        """
        while True:
            pressed_key = input(
                '-----> Type "y" to USE LOCAL FILE or "n" to CALL API and press ENTER: '
            )
            logging.info("")
            if pressed_key.lower() == "y":
                logging.info("Info: You pressed 'y' - to use local file \n")
                return True

            if pressed_key.lower() == "n":
                logging.info("Info: You pressed 'n' -  to call api for new file \n")
                return False
            logging.info("Info: Wrong key, please try again \n")

    @staticmethod
    def print_start_menu():
        """Main function"""
        CliMenu.print_logo()
        CliMenu.print_banner()
        CliMenu.print_options()
        logging.info("\n")
