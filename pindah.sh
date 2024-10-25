#!/bin/bash

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Path to the directory containing the profiles.ini file
PROFILES_INI_DIR="$(dirname "$0")"
PROFILES_INI="$PROFILES_INI_DIR/profiles.ini"

# Check if the profiles.ini file exists
if [[ ! -f $PROFILES_INI ]]; then
    echo -e "${RED}Profiles file '$PROFILES_INI' not found!${NC}"
    exit 1
fi

# Create a new profile based on existing profiles
while IFS= read -r LINE; do
    if [[ $LINE =~ ^\[Profile[0-9]+\] ]]; then
        # Get the profile section
        PROFILE_SECTION="${LINE:1:-1}"
        
        # Read the next lines for Name and Path
        read -r NAME_LINE
        read -r ISREL_LINE
        read -r PATH_LINE
        
        # Extract Name and Path
        PROFILE_NAME="${NAME_LINE#*=}"
        PROFILE_PATH="${PATH_LINE#*=}"

        # Adjust the path if it's relative
        OLD_PROFILE_DIR="$PROFILES_INI_DIR/$PROFILE_PATH"

        # Check if the profile directory exists
        if [[ -d $OLD_PROFILE_DIR ]]; then
            # Create a new profile using the Firefox command
            NEW_PROFILE_NAME="${PROFILE_NAME}_Copy"
            firefox -CreateProfile "$NEW_PROFILE_NAME" > /dev/null 2>&1
            
            # Wait a moment to allow the directory to be created
            sleep 1
            
            # Find the newly created profile directory
            NEW_PROFILE_DIR=$(find "$HOME/.mozilla/firefox" -maxdepth 1 -type d -name "*${NEW_PROFILE_NAME}*")

            # Check if we found the new profile directory
            if [[ -d $NEW_PROFILE_DIR ]]; then
                echo -e "${GREEN}Copying data from profile '$OLD_PROFILE_DIR' to '$NEW_PROFILE_NAME'...${NC}"
                cp -r "$OLD_PROFILE_DIR/"* "$NEW_PROFILE_DIR/"
                echo -e "${GREEN}Data copied successfully to '$NEW_PROFILE_NAME'.${NC}"
            else
                echo -e "${RED}Failed to create or find profile '$NEW_PROFILE_NAME'.${NC}"
            fi
        else
            echo -e "${RED}Profile at '$OLD_PROFILE_DIR' does not exist!${NC}"
        fi
    fi
done < "$PROFILES_INI"

echo -e "${GREEN}Data copying process complete.${NC}"