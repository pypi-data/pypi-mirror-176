from prometheus_aioexporter import PrometheusExporterScript, MetricConfig

from .stream import Stream


class Helios(PrometheusExporterScript):
    name = "helios-monitor"
    default_port = 3010

    def configure_argument_parser(self, parser):
        parser.add_argument("stream", help="The stream to monitor")

    def configure(self, args):
        self.stream = args.stream
        self.stream_name = self.stream.rsplit("/", 1)[-1]
        self.create_metrics([
            MetricConfig("stream_ebu_r128",
                          "stream loudness measured with EBU-R128",
                          "gauge",
                          {
                              "labels": ["stream", "job"]
                          })
        ])
        self.current_chunk = None
        self.logger.info("Monitor configured")

    async def on_application_startup(self, application):
        application["exporter"].set_metric_update_handler(self._update_handler)
        self.reader_thread = Stream(args=(self.stream,), kwargs={"logger": self.logger})
        self.reader_thread.start()

    async def on_application_shutdown(self, application):
        self.logger.info("Shutdown received")
        self.reader_thread.is_running = False
        self.reader_thread.join()

    async def _update_handler(self, metrics):
        value = self.reader_thread.current_line
        self.logger.debug(f"Got value: {value}")
        if value != None:
            metrics['stream_ebu_r128'].labels(
                stream=self.stream,
                job="helix"
            ).set(value)
