from middleware.protocol import read_json
from common.data_publisher import DataPublisher
from common.synchronizer import Synchronizer
import logging
import common.config as config

class DataReceiver:
    def __init__(self):
        self.data_publisher = DataPublisher()
        self.synchronizer = Synchronizer()

    def data_receiver(self, skt):
        data_publisher = self.data_publisher
        data, extra = read_json(skt)
        logging.info('sending data')
        # while extra != "finished" and extra != "error":
        while extra != config.FINISHED_MESSAGE and extra != config.ERROR_MESSAGE:
            # if extra == "end of stations":
            if extra == config.END_STATIONS_MESSAGE:
                logging.info('sending end of stations')
                data_publisher.send_end_stations()
            # elif extra == "end of weather":
            elif extra == config.END_WEATHER_MESSAGE:
                logging.info('sending end of weather, syncying')
                data_publisher.send_end_weather()
                self.synchronizer.sync()
                logging.info('sending end of weather, syncying finished')
            else:
                data_publisher.publish(data)
            data, extra = read_json(skt)
        data_publisher.send_end_trips()
        return extra
    
    def close(self):
        self.data_publisher.close()
