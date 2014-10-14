/**
   @file rtc-clear.c

   rtc-clear is a tool to clear pending RTC wake up. It is based on dsmetool.c
   in dsme project: https://github.com/nemomobile/dsme

   <p>

   Copyright (C) 2014 Jolla Oy
   Copyright (C) 2004-2011 Nokia Corporation.

   @author Ismo Laitinen <ismo.laitinen@nokia.com>
   @author Semi Malinen <semi.malinen@nokia.com>
   @author Matias Muhonen <ext-matias.muhonen@nokia.com>
   @author Kalle Jokiniemi <kalle.jokiniemi@jolla.com>

   rtc-clear is free software; you can redistribute it and/or modify
   it under the terms of the GNU Lesser General Public License
   version 2.1 as published by the Free Software Foundation.

   rtc-clear is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public
   License along with rtc-clear.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>
#include <getopt.h>

#include <sys/ioctl.h>

#include <linux/rtc.h>

static const char *help = {
"  clear-rtc - tool for clearing any pending RTC wake ups.\n"
"  Usage:\n"
"    clear-rtc [OPTIONS]\n"
"  OPTIONS:\n"
"    --help      Display help\n"
};

static struct option options[] = {
	{"help",    no_argument,       0,  0 },
	{0,         0,                 0,  0 },
};


void print_help(void)
{
	printf("%s", help);
}

static int clear_rtc(void)
{
  /* Clear possible RTC alarm wakeup*/

    static const char rtc_path[] = "/dev/rtc0";
    int rtc_fd = -1;
    struct rtc_wkalrm alrm;

    if ((rtc_fd = open(rtc_path, O_RDONLY)) == -1) {
        /* TODO:
         * If open fails reason is most likely that dsme is running and has opened rtc.
         * In that case we should send message to dsme and ask it to do the clearing.
         * This functionality is not now needed because rtc alarms are cleared
         * only during preinit and there dsme is not running.
         * But to make this complete, that functionality should be added.
         */
        printf("Failed to open %s: %m\n", rtc_path);
        return EXIT_FAILURE;
    }

    memset(&alrm, 0, sizeof(alrm));
    if (ioctl(rtc_fd, RTC_WKALM_RD, &alrm) == -1) {
        printf("Failed to read rtc alarms %s: %s: %m\n", rtc_path, "RTC_WKALM_RD");
        close(rtc_fd);
        return EXIT_FAILURE;
    }
    printf("Alarm was %s at %d.%d.%d %02d:%02d:%02d UTC\n",
           alrm.enabled ? "Enabled" : "Disabled",
           1900+alrm.time.tm_year, 1+alrm.time.tm_mon, alrm.time.tm_mday, 
           alrm.time.tm_hour, alrm.time.tm_min, alrm.time.tm_sec);

    /* Because of bug? we need to enable alarm first before we can disable it */
    alrm.enabled = 1;
    alrm.pending = 0;
    if (ioctl(rtc_fd, RTC_WKALM_SET, &alrm) == -1)
        printf("Failed to enable rtc alarms %s: %s: %m\n", rtc_path, "RTC_WKALM_SET");
    /* Now disable the alarm */
    alrm.enabled = 0;
    alrm.pending = 0;
    if (ioctl(rtc_fd, RTC_WKALM_SET, &alrm) == -1) {
        printf("Failed to clear rtc alarms %s: %s: %m\n", rtc_path, "RTC_WKALM_SET");
        close(rtc_fd);
        return EXIT_FAILURE;
    }
    close(rtc_fd);
    printf("RTC alarm cleared ok\n");
    return EXIT_SUCCESS;
}

int main(int argc, char * argv[])
{
	int c;
	int opt_index = 0;

	while (1) {

		c = getopt_long(argc, argv, "h", options, &opt_index);
		if (c == -1)
			break;

		switch (c) {
		case 'h':
			print_help();
			return EXIT_SUCCESS;
			break;
		default:
			printf("Invalid option \"%c\"\n", c);
			print_help();
			return EXIT_FAILURE;
			break;
		}
	}
	return clear_rtc();
}



