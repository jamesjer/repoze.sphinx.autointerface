import unittest

from .util import TestApp

from .. import autointerface
from sphinx.ext.autodoc import AutoDirective, ALL

from docutils.statemachine import ViewList

from zope import interface

class IPlumbusMaker(interface.Interface):

    grumbo = interface.Attribute("The dinglebop is fed through here")
    fleeb = interface.Attribute("The dinglebop is polished with this")

    def smoothTheDinglebop(schleem):
        """
        Smooth it out.

        The schleem is then repurposed.
        """

class Options(object):
    inherited_members = False
    undoc_members = False
    private_members = False
    special_members = False
    imported_members = False
    show_inheritance = False
    noindex = False
    annotation = None
    synopsis = ''
    platform = ''
    deprecated = False
    members = ()
    member_order = 'alphabetic'
    exclude_members = ()

    def __init__(self):
        self.exclude_members = set()
        self.members = []

class Directive(object):
    env = None
    genopt = None
    result = None

    def __init__(self):
        self._warnings = []
        self.filename_set = set()
        self.result = ViewList()

    def warn(self, msg):
        self._warnings.append(msg)

class TestAutoInterface(unittest.TestCase):

    def setUp(self):
        app = self.app = TestApp()
        app.builder.env.app = app
        app.builder.env.temp_data['docname'] = 'dummy'

        autointerface.setup(app)

        opt = self.options = Options()
        d = self.directive = Directive()
        d.env = app.builder.env
        d.genopt = opt


    def tearDown(self):
        self.app.cleanup()
        self.app = None

    def assertResultContains(self, item,
                             objtype='interface', name='repoze.sphinx.tests.test_autointerface.IPlumbusMaker',
                             **kw):
        directive = self.directive
        inst = AutoDirective._registry[objtype](directive, name)
        inst.generate(**kw)
        # print '\n'.join(directive.result)
        self.assertEqual([], directive._warnings)
        self.assertIn(item, directive.result)
        results = directive.result[:]
        del directive.result[:]
        return '\n'.join(results)

    def test_restricted_members(self):
        self.options.members = ['smoothTheDinglebop']
        all_results = self.assertResultContains('   .. method:: smoothTheDinglebop(schleem)')
        self.assertNotIn('grumbo', all_results)

    def test_all_members(self):
        self.options.members = ALL
        all_results = self.assertResultContains('   .. method:: smoothTheDinglebop(schleem)')
        self.assertIn('grumbo', all_results)
        self.assertIn('fleeb', all_results)
