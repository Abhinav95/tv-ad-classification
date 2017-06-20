# C. Tag commercials

# Written by FFS on 14 Oct 2013
#
# Dependencies: sponge (moreutils)
#
# Changelog:
#
#	2014-06-24 Use extension txt2 on hoffman
#	2014-04-12 Corner case -- tag ends in commercial
#	2014-04-11 Fix failure to detect POP only
#	2014-02-26 Skip triple chevrons in CC3 lines (Spanish)
#       2014-02-23 Add story boundary on triple chevrons
#	2014-01-05 Use the start of the next story rather than the end of the POP to define the commercial block
#
#------------------------------------------------------------------------------------

# What does this third section do
# echo -e "\n\tConvert caption style information to segment tags for commercials"
# echo -e "\tand add story start tags before triple chevrons (>>>)."
# echo -e "\n\tThe original file is given the extension cs (caption styles)."

# Verify extension
#if [ ! -f $FIL.txt2 ] ; then echo -e "\n\tThe commercial tagger processes .txt2 files.\n" ; exit ; fi


# Process files that have caption styles and triple chevrons
if [ "$( egrep -m 1 "\|RU2\||\|RU3\||\|POP\||\|>>>" $FIL.txt2 )" ] ; then

  # Welcome
  echo -en "\tCreating commercial and story tags for $FIL.txt2\t"

  # Host system
  HOST="$( hostname -s )"

  # File length
  NLIN="$( cat $FIL.txt2 | wc -l )"

  # Internal field separator
  OFS=$IFS

  # Examine the file a line at a time
  for N in `seq 1 $NLIN` ; do

    # Debug
    #if [ "$N" -gt "20" ] ; then break ; fi

    # Capture the line
    read LIN <<< $( sed -n "$N p" $FIL.txt2 )

    # At the end of the file
    if [ "${LIN:0:3}" = "END" ] ; then

      # If we end in the middle of a commercial (corner case)
      if [ "$SAD" != "" -a "$EAD" != "" ] ; then

        # Use the end time of the last POP line
        SEG="$SAD|$EAD|SEG_00|Type=Commercial"

        # Insert the commercial block tag before the start
        sed -i "1,/^$SAD|$SEAD/ {/^$SAD|$SEAD/i\
$SEG
}" $FIL.txt3
        SAD="" ; EAD="" ; echo -en "."
      fi

      # Write the END line
      echo -e "$LIN" >> $FIL.txt3 ; continue
    fi

    # Keep the lines that start with a letter (header)
    if [[ "${LIN:0:1}" =~ [A-Z] ]] ; then echo -e "$LIN" >> $FIL.txt3 ; continue ; fi
   #if [[ "${LIN:0:1}" =~ [A-Z] ]] ; then echo -e "$LIN" | tee -a $FIL.txt3 ; continue ; fi

    # Capture the field values in each line (for all other lines) in an array
    IFS=$'\n' ; FLD=( $( echo "$LIN" | sed -e 's/|/\n/g' ) )

    # Rewrite non-commercial lines
    if [ "${FLD[3]}" != "POP" ] ; then

      # Initial story start
      if [ -z "$FIRST" ] ; then FIRST=$N ; echo "${FLD[0]}|${FLD[1]}|SEG_00|Type=Story start" >> $FIL.txt3

        # Get the starting timestamp of a triple chevron (>>>) indicating a story boundary -- but not in US Spanish files
        #elif [[ "${FLD[4]}" =~ ">>>" && "${FLD[2]}" != "CC3" && $FIL != *KMEX* ]] ; then echo "${FLD[0]}|${FLD[1]}|SEG_00|Type=Story start" >> $FIL.txt3
        elif [[ "${FLD[4]}" =~ ">>>" && "${FLD[2]}" != "CC3" ]] ; then echo "${FLD[0]}|${FLD[1]}|SEG_00|Type=Story start" >> $FIL.txt3

      fi

      echo "${FLD[0]}|${FLD[1]}|${FLD[2]}|${FLD[4]}" >> $FIL.txt3
    fi

    # Get the start and end time of the first line of the commercial
    if [ "${FLD[3]}" = "POP" -a "$SAD" = "" ] ; then SAD="${FLD[0]}" SEAD="${FLD[1]}" ; fi

    # Rewrite the commercial lines and store the successive end times
    if [ "${FLD[3]}" = "POP" ] ; then echo "${FLD[0]}|${FLD[1]}|${FLD[2]}|${FLD[4]}" >> $FIL.txt3 ; EAD="${FLD[1]}" ; fi

    # Debug
    #echo -e "\n\t{FLD[3]} is ${FLD[3]} and EAD is $EAD\n"

    # Get the end of the commercial
    if [ "${FLD[3]}" != "POP" -a "$EAD" != "" ] ; then

      # Either use the end time of the last POP line
      #SEG="$SAD|$EAD|SEG_00|Type=Commercial"

      # Or better, the start time of the first non-POP line
      SEG="$SAD|${FLD[0]}|SEG_00|Type=Commercial"

      # Insert the commercial block tag before the start
      sed -i "1,/^$SAD|$SEAD/ {/^$SAD|$SEAD/i\
$SEG
}" $FIL.txt3
      SAD="" ; EAD="" ; echo -en "."

      # At the same time, insert a single story start tag at the end of the commercial
      SEG="${FLD[0]}|${FLD[1]}|SEG_00|Type=Story start"
      sed -i "1,/^${FLD[0]}|${FLD[1]}/ {/^${FLD[0]}|${FLD[1]}/i\
$SEG
}" $FIL.txt3

    fi

  done

fi

# Internal field separator
IFS=$OFS

# For files that had no caption styles
if [ ! -e $FIL.txt3 ] ; then cp -p $FIL.txt2 $FIL.txt3 ; fi

# Remove duplicate lines (SEG lines after POP and before >>>)
uniq $FIL.txt3 | $HOME/bin/sponge $FIL.txt3

# Receipt
if [ -s $FIL.txt3 ] ; then TAGS="$( grep -c SEG_00 $FIL.txt3 )" ; else SIZE=0 ; fi
echo -e "`date +%F\ %H:%M:%S` \t${SCRIPT%.*} \t$QNUM\t$HOST \tCommercials \t$TAGS tags  \t$FIL.txt3" | tee -a $LOGS/reservations.$( date +%F )

# EOF