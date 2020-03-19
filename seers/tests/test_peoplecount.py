import unittest
import seer_config
import seer_plugin
import plugins.people_count


class TestPeopleCountPlugin(unittest.TestCase):
    MODEL_PATH = 'MobileNetSSD_deploy.caffemodel'
    PROTO_PATH = 'MobileNetSSD_deploy.prototxt.txt'
    STREAM_TYPE = 'file'
    FILE_STREAM_PATH = 'tests/test_vid.mp4'

    def setUp(self):
        seer_config.configuration[plugins.people_count.PeopleCount.INI][
            plugins.people_count.PeopleCount.STREAM_TYPE_INI] = TestPeopleCountPlugin.STREAM_TYPE
        seer_config.configuration[plugins.people_count.PeopleCount.INI][
            plugins.people_count.PeopleCount.FILE_STREAM_PATH_INI] = TestPeopleCountPlugin.FILE_STREAM_PATH

    def test_collect(self):
        seer_config.configuration[plugins.people_count.PeopleCount.INI][
            plugins.people_count.PeopleCount.MODEL_INI] = TestPeopleCountPlugin.MODEL_PATH
        seer_config.configuration[plugins.people_count.PeopleCount.INI][
            plugins.people_count.PeopleCount.PROTOTXT_INI] = TestPeopleCountPlugin.PROTO_PATH

        def testing_collect(deliv, data):
            count_data = data.get(plugins.people_count.PeopleCount.COUNT_KEY)
            self.assertIsInstance(count_data, int)
            deliv.stop()

        delivery = seer_plugin.PluginDelivery([plugins.people_count.PeopleCount],
                                              testing_collect, timeout=None)

        delivery.start()

    def test_init_missing_model(self):
        seer_config.configuration[plugins.people_count.PeopleCount.INI][plugins.people_count.PeopleCount.MODEL_INI] = ''

        def testing_init(deliv, data):
            self.assertFalse(
                plugins.people_count.PeopleCount.COUNT_KEY in data)
            deliv.stop()

        delivery = seer_plugin.PluginDelivery([plugins.people_count.PeopleCount],
                                              testing_init, timeout=5000)

        delivery.start()

    def test_init_missing_prototxt(self):
        seer_config.configuration[plugins.people_count.PeopleCount.INI][plugins.people_count.PeopleCount.PROTOTXT_INI] = ''

        def testing_init(deliv, data):
            self.assertFalse(
                plugins.people_count.PeopleCount.COUNT_KEY in data)
            deliv.stop()

        delivery = seer_plugin.PluginDelivery([plugins.people_count.PeopleCount],
                                              testing_init, timeout=5000)

        delivery.start()
