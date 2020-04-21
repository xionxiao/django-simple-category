from django.test import TestCase
from exam.models import QuizCategory
from category.models import BaseCategory


class CategoryTestCase(TestCase):
    cats = [
        ['语文'],
        ['数学'],
        ['数学', '代数'],
        ['数学', '几何'],
        ['数学', '几何', '立体几何'],
        ['数学', '几何', '立体几何', '平面几何'],
        ['数学', '几何', '解析几何'],
        ['物理'],
        ['化学'],
    ]

    @classmethod
    def setUpTestData(cls):
        import random
        # Create all the categories disordered
        random.shuffle(cls.cats)
        for cs in cls.cats:
            parent = None
            for c in cs:
                parent = QuizCategory.objects.update_or_create(
                    name=c, parent=parent)[0]

    def test_creation(self):
        qs = QuizCategory.objects.all()
        self.assertEqual(qs.count(), len(self.cats))

    def test_root_nodes(self):
        # test nodes name of root nodes
        qs = QuizCategory.objects.filter(parent=None)
        for q in qs:
            self.assertEqual(int(q.nodes), int(q.id))
            self.assertEqual(q.full_name, q.name)
            self.assertFalse(q.get_ancestors())
            self.assertEqual(q.nodes, q._expand_node(q.id))

    # test _expand_node and _split_node functions
    def test_epand_node(self):
        qs = QuizCategory.objects.all()
        for q in qs:
            sp = q._split_nodes()[-1]
            ep = q._expand_node(q.id)
            self.assertEqual(sp, ep)

    # test get_ancestors
    def test_get_ancestors(self):
        qs = QuizCategory.objects.all()
        for q in qs:
            parents = []
            p = q.parent
            while p is not None:
                if not p in parents:
                    parents.append(p)
                    p = p.parent
                else:
                    self.assertTrue(False, 'loop in ancestors')

            self.assertEqual(list(q.get_ancestors()), list(reversed(parents)))

    # test get_descendants
    def test_descendants(self):
        qs = QuizCategory.objects.all()
        for q in qs:
            cs = q.children.all()
            while True:
                plus = cs | qs.filter(parent__in=cs)
                if list(plus) != list(cs):
                    cs = plus
                else:
                    break
            cs = cs.order_by('id')
            des = q.get_descendants().order_by('id')
            self.assertEqual(list(cs), list(des))

    def test_modify_parent(self):
        q = QuizCategory.objects.get(name='几何')
        p = QuizCategory.objects.get(name='语文')
        pre = q.parent
        q.parent = p
        q.save()
        q.refresh_from_db()
        self.assertEqual(list(q.get_ancestors()), [p])
        self.assertEqual(q.nodes, p.nodes + q._expand_node(q.id))
        self.assertEqual(q.full_name, '语文->几何')
        ds = q.get_descendants()
        for d in ds:
            # self.assertEqual(d.full_name, q.full_name + '->' + d.name)
            self.assertTrue(p in d.get_ancestors())
            self.assertTrue(q in d.get_ancestors())
            self.assertFalse(pre in d.get_ancestors())

    def test_modify_parent_with_loop(self):
        q = QuizCategory.objects.get(name='几何')
        p = QuizCategory.objects.get(name='立体几何')
        q.parent = p
        self.assertRaises(ValueError, q.save)
