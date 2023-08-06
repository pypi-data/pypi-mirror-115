from collections import OrderedDict


class ColorTag(object):
    """
    Object to be passed into Verbose class methods to append colorized tags to the
    start of a message printed to console.
    """
    def __init__(self):
        # Pairs of tag_name: tag_color. Color to be passed into `click.style()`
        self.color_map = {
            'dry-run': 'magenta',
            'full-refresh': 'red',
            'step-name': 'blue',

            # Transform step names
            'contact-aggregated-stats': 'blue',
            'emoji-text-map': 'blue',
            'message-emoji-map': 'blue',
            'message-tokens': 'blue',
            'tokens': 'blue',
        }

        # Paris of tag_name: tag_color
        self.stack = OrderedDict()

    def add(self, tag_name):
        """Add a tag to stack."""
        self._assert_valid_tag(tag_name)
        if not self.has(tag_name):
            self.stack[tag_name] = self.color_map[tag_name]

    def has(self, tag_name):
        """Indicate logically whether a particular tag name is in stack."""
        return tag_name in self.stack.keys()

    def remove(self, tag_name):
        """Attempt to remove a tag from stack."""
        assert tag_name in self.stack.keys(), f"Tag '{tag_name}' not in stack"
        self.stack = OrderedDict({k: v for k, v in self.stack.items() if k != tag_name})

    def reset(self):
        """Clear all tags from stack."""
        self.stack = OrderedDict()

    def _assert_valid_tag(self, tag_name):
        """
        Check whether a tag is present in color map. Otherwise, it's an invalid tag unless
        added to the color map.
        """
        msg = f"Tag '{tag_name}' not in color map. Acceptable tags are: {', '.join(list(self.color_map.keys()))}"
        assert tag_name in self.color_map.keys(), msg
