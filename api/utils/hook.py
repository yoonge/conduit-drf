from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject

class HookSerializer(object):

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = {}
        fields = self._readable_fields

        for field in fields:
            if hasattr(self, 'hk_%s' % field.field_name):
                val = getattr(self, 'hk_%s' % field.field_name)(instance)
                ret[field.field_name] = val
            else:
                try:
                    attribute = field.get_attribute(instance)
                except SkipField:
                    continue

                # We skip `to_representation` for `None` values so that fields do
                # not have to explicitly deal with that case.
                #
                # For related fields with `use_pk_only_optimization` we need to
                # resolve the pk value.
                check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
                if check_for_none is None:
                    ret[field.field_name] = None
                else:
                    ret[field.field_name] = field.to_representation(attribute)

        return ret
