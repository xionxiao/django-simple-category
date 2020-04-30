from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.db.models.functions import Replace


class BaseCategory(models.Model):
    '''
    Abstract Category Model
    '''

    NODE_FIELD_WIDTH = 256
    NODE_ID_WIDTH = 8
    JOINT_SYMBOL = '->'

    name = models.CharField(max_length=100, verbose_name=_('name'))

    full_name = models.CharField(max_length=255,
                                 blank=True,
                                 default='',
                                 verbose_name=_("full_name"))

    parent = models.ForeignKey('self',
                               models.CASCADE,
                               blank=True,
                               null=True,
                               related_name='children',
                               verbose_name=_("parent"))

    # nodes
    nodes = models.CharField(max_length=NODE_FIELD_WIDTH,
                             verbose_name=_("nodes"),
                             editable=False,
                             blank=True,
                             default="")

    class Meta:
        abstract = True
        ordering = ('nodes', 'id')
        unique_together = ('name', 'parent')

    def _split_nodes(self):
        # split nodes per 8 bit
        return list(map(''.join,
                        zip(*[iter(self.nodes)] * self.NODE_ID_WIDTH)))

    def _expand_node(self, ss):
        return str(ss).zfill(self.NODE_ID_WIDTH)

    def _check_ancestor_loops(self):
        if self.parent and self in self.parent.get_ancestors():
            raise ValueError(_("detect loop in categories."))

    def get_ancestors(self):
        return self.__class__.objects.filter(
            id__in=self._split_nodes()).exclude(id=self.id).order_by('nodes')

    def get_descendants(self):
        return self.__class__.objects.filter(
            nodes__startswith=self.nodes).exclude(id=self.id).order_by('nodes')

    def clean(self):
        try:
            self._check_ancestor_loops()
        except ValueError as e:
            raise ValidationError(str(e))
        return super().clean()

    def save(self, *args, **kwargs):
        self._check_ancestor_loops()
        if not self.id:
            last = self.__class__.objects.order_by('id').last()
            self.id = last.id + 1 if last else 1
        node = self._expand_node(self.id)
        ds = self.get_descendants()
        if self.parent:
            self.nodes = self.parent.nodes + node
            self.full_name = self.JOINT_SYMBOL.join(
                [self.parent.full_name, self.name])
        else:
            self.nodes = node
            self.full_name = self.name

        super().save(*args, **kwargs)

        [d.save() for d in ds]

    def __str__(self):
        return self.name
