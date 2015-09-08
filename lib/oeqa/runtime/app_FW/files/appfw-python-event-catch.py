import argparse
import glib
import json
import logging
import appfw
import time

logger = logging.getLogger("__event-catch__")

ml = glib.MainLoop(None)

def event_cb(event, data):

        logger.debug("Received an event with event = " + str(event) + \
                     ", data = " + str(data))
        if (event == 'system::terminate'):
                logger.info("Received a SIGTERM, quitting mainloop...")
                ml.quit()
        elif (event == 'system::reload'):
                logger.info("Received SIGHUP, doing nothing...")


def subscribe_status(seqno, status, msg, data, user_data):
	if status == 0:
		logger.debug("Succesfully subscribed for events.")
	else:
		if msg == None:
			msg = "<unknown error>"
		logger.debug("Event subscription failed (" + str(status) + ": " + \
		             msg + ").")

def main():
	#Parse arguments
	parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--signals", action="store_true", help="bridge system signals as events")
	parser.add_argument("-e", "--events", type=str, help="events to send/subscribe for")
	parser.add_argument("-d", "--debug", action="count", default=0, help="enable given debug configuration")
	args = parser.parse_args()

	app = appfw.IotApp()


	if args.debug > 0:
		if args.debug >= 1:
	                logging.basicConfig(filename="/opt/appfw_test/appfw_test.log")
			logger.setLevel(logging.DEBUG)
		if args.debug >= 2:
			app._enable_debug([""])
		if args.debug >= 3:
			app._enable_debug(["@python-app-fw-wrapper.cpp"])
		if args.debug > 3:
			app._enable_debug(["*"])

	logger.debug(args)

	#Set the status callback
	app.status_handler = subscribe_status

	if (args.signals):
		app.enable_signals()
        if args.events: 
            if ',' in args.events :
	        args.events = args.events.split(',')
	        #Set event subscriptions
	        app.subscriptions = set(args.events)
            else:
	        app.subscriptions = args.events

	#Set event callback
	app.event_handler = event_cb

	#Start mainloop
	ml.run()

if __name__ == "__main__":
        main()
