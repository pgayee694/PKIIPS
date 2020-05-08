import unittest
from unittest.mock import patch
from app.plugins.distance_plugin import DistanceAnalyzerPlugin

class DistanceAnalyzerTest(unittest.TestCase):
    """
    Tests the distance analyzer plugin
    """

    def setUp(self):
        engine_patcher = patch('app.plugins.distance_plugin.global_model_engine')
        self.mock_engine = engine_patcher.start()
        self.addCleanup(engine_patcher.stop)
        self.mock_engine.update_data.return_value = True

    def test_constructor(self):
        analyzer = DistanceAnalyzerPlugin()

        self.assertEqual(set(['id_', 'room', 'range_', 'count', 'distances']), analyzer.get_data_keywords())
        self.assertEqual(set(), analyzer.get_constraint_keywords())

    def test_init(self):
        analyzer = DistanceAnalyzerPlugin()
        analyzer.init()

        self.assertEqual([], analyzer.seers)

    def test_shutdown(self):
        analyzer = DistanceAnalyzerPlugin()
        analyzer.init()

        analyzer.shutdown()
        self.assertEqual(None, analyzer.seers)
    
    def test_collect(self):
        analyzer = DistanceAnalyzerPlugin()
        analyzer.init()
        s1 = DistanceAnalyzerPlugin.PeopleCount('0', '269', 610, 3, [100,200,300])
        s2 = DistanceAnalyzerPlugin.PeopleCount('1', '269', 610, 2, [300,600])
        s3 = DistanceAnalyzerPlugin.PeopleCount('0', '250', 100, 1, [30])
        analyzer.seers = [s1,s2,s3]
        expected = {
            'Counts': 
            {
                '269': 5,
                '250': 1
            }
        }

        actual = analyzer.collect()

        self.assertDictEqual(expected, actual)
    
    def test_analyze_new_room_new_id(self):
        analyzer = DistanceAnalyzerPlugin()
        analyzer.init()
        s1 = DistanceAnalyzerPlugin.PeopleCount('0', '269', 610, 3, [100,200,600])

        analyzer.analyze(s1)

        self.mock_engine.update_data.assert_called_once()
        self.mock_engine.update_data.assert_called_with({
            'Room': '269',
            'Count': 3
        })
        self.assertCountEqual(analyzer.seers, [s1])
    
    def test_analyze_old_room_new_id(self):
        analyzer = DistanceAnalyzerPlugin()
        analyzer.init()
        s1 = DistanceAnalyzerPlugin.PeopleCount('0', '269', 610, 3, [100,200,600])
        analyzer.seers.append(s1)
        s2 = DistanceAnalyzerPlugin.PeopleCount('1', '269', 610, 3, [700, 800, 900])

        analyzer.analyze(s2)

        self.mock_engine.update_data.assert_called_once()
        self.mock_engine.update_data.assert_called_with({
            'Room': '269',
            'Count': 3
        })
        self.assertCountEqual(analyzer.seers, [s1, s2])
    
    def test_analyze_old_room_old_id(self):
        analyzer = DistanceAnalyzerPlugin()
        analyzer.init()
        s1 = DistanceAnalyzerPlugin.PeopleCount('0', '269', 610, 3, [100,200,600])
        analyzer.seers.append(s1)
        s2 = DistanceAnalyzerPlugin.PeopleCount('0', '269', 610, 3, [700, 800, 900])

        analyzer.analyze(s2)

        self.mock_engine.update_data.assert_called_once()
        self.mock_engine.update_data.assert_called_with({
            'Room': '269',
            'Count': 0
        })

        s1.count = 0 # python tries to compare object references instead of values
        self.assertListEqual(analyzer.seers, [s1])