
import graph, unittest


class TestGraphModule(unittest.TestCase):
	def setUp(self):
		self.graph_types=[graph.graph,graph.hashgraph]

	def test_nodelist_for_graph(self):
		g=graph.graph()
		self.assertEqual(g.nodelist(),[])
		g.insertnode(0)
		self.assertEqual(g.nodelist(),[0])
		for i in [1,2,3,'hi']:
			g.insertnode(i)
		self.assertEqual(g.nodelist(),[0,1,2,3,'hi'])
		g.insertedge(0,2)
		self.assertEqual(g.nodelist(),[0,1,2,3,'hi'])
		g.deletenode(0)
		self.assertEqual(g.nodelist(),[1,2,3,'hi'])
		g.deletenode(2)
		self.assertEqual(g.nodelist(),[1,3,'hi'])
		g.relabel(3,[0,0,2])
		self.assertEqual(g.nodelist(),[1,[0,0,2],'hi'])

	def test_node_membership(self):
		nl=[1,2,3,4,5,'sure','ok','great']
		non_nl=[6,7,0,8,'bummer','not quite',-1,100,'ouch']
		el=[(2,3),(1,5),('ok',4)]
		for typ in self.graph_types:
			g=typ(nl,el)
			for i in nl:
				self.assertIn(i,g)
			for i in non_nl:
				self.assertNotIn(i,g)

	def test_graphical_fn(self):
		graphical=graph.graphical
		self.assertTrue (graphical([1,1]))
		self.assertTrue (graphical([2,3,1,2]))
		self.assertFalse (graphical([5,4,1,6]))
		self.assertFalse (graphical([2,2,3,2,1,1,4,0]))
		self.assertTrue (graphical([6,6,5,5,4,4,1,1]))
		self.assertTrue (graphical([6,6,4,4,3,3,2,2]))
		self.assertFalse (graphical([6]*3+[4]*3+[2]*5+[1]))


if __name__=='__main__':
	unittest.main()
