#!/bin/sh

INITFS_ARCHIVE=/usr/share/hw-ramdisk/initfs.tar.bz2
INIT_FILE=NULL
BIN_FILES=NULL

print_usage()
{
echo    "Usage: $0 -w <work-dir> [-t <tools-to-be-added>] [-i <custom-init>]"
}

#
# get commandline parameters
#
echo
echo "Options:"
while getopts "w:t:i:" opt; do
	case $opt in
	w)
		WORK_DIR=$OPTARG
		echo "Working directory: \"$WORK_DIR\""
		;;
	t)
		BIN_FILES=$OPTARG
		echo "Binary tool files: \"$BIN_FILES\""
		;;
	i)
		INIT_FILE=$OPTARG
		echo "Init script: \"$INIT_FILE\""
		;;

	\?)
		print_usage
		exit 1
		;;
	esac
done

#Check parameters.
[ -z "$WORK_DIR" ] && {
	print_usage
	exit 1
}

[ -d "$WORK_DIR" ] || {
	echo "Working directory \"$WORK_DIR\" does not exist"
	exit 1
}

# Extract the initial moslo-build directory structure and files
[ -e "$INITFS_ARCHIVE" ] || {
	echo "Cannot find initfs archive \"$INITFS_ARCHIVE\""
	exit 1
}

UTILS_FILE=$WORK_DIR/initfs/skeleton/util-list

# add_files(list-of-files, util-list-file)
add_files()
{
	for i in $BIN_FILES
	do
		echo Adding $i
		if [ ! -e $i ]; then
			echo "add_files: \"$i\" does not exist"
			return 1
		fi
		if ! grep -r $i $UTILS_FILE; then
			#File was missing, let's add it
			echo "$i" >> $UTILS_FILE
		fi
	done
	return 0
}

tar -xjf $INITFS_ARCHIVE -C $WORK_DIR

# Add user provided tools and files to the filesystem
[ "$BIN_FILES" == "NULL" ] || {
	add_files
	RET=$?
	if [ ! $RET -eq 0 ]; then
		exit 1
	fi
}

# Replace init with user provided init
[ $INIT_FILE == "NULL" ] || {
	install -m 755 -D $INIT_FILE $WORK_DIR/initfs/skeleton/init
}

echo "Initialized initrd generation setup to \"$WORK_DIR\""

