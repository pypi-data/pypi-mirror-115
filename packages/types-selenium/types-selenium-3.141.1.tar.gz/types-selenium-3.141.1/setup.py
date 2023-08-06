from setuptools import setup

name = "types-selenium"
description = "Typing stubs for selenium"
long_description = '''
## Typing stubs for selenium

This is a PEP 561 type stub package for the `selenium` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `selenium`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/selenium. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `6ccf5e7d6563b0b27a98d8a008f07dc4d4e39a2d`.
'''.lstrip()

setup(name=name,
      version="3.141.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['selenium-stubs'],
      package_data={'selenium-stubs': ['__init__.pyi', 'common/__init__.pyi', 'common/exceptions.pyi', 'webdriver/__init__.pyi', 'webdriver/chrome/__init__.pyi', 'webdriver/chrome/options.pyi', 'webdriver/chrome/remote_connection.pyi', 'webdriver/chrome/webdriver.pyi', 'webdriver/chrome/service.pyi', 'webdriver/android/__init__.pyi', 'webdriver/android/webdriver.pyi', 'webdriver/remote/file_detector.pyi', 'webdriver/remote/mobile.pyi', 'webdriver/remote/__init__.pyi', 'webdriver/remote/utils.pyi', 'webdriver/remote/command.pyi', 'webdriver/remote/webelement.pyi', 'webdriver/remote/switch_to.pyi', 'webdriver/remote/remote_connection.pyi', 'webdriver/remote/errorhandler.pyi', 'webdriver/remote/webdriver.pyi', 'webdriver/blackberry/__init__.pyi', 'webdriver/blackberry/webdriver.pyi', 'webdriver/safari/__init__.pyi', 'webdriver/safari/remote_connection.pyi', 'webdriver/safari/webdriver.pyi', 'webdriver/safari/permissions.pyi', 'webdriver/safari/service.pyi', 'webdriver/support/select.pyi', 'webdriver/support/__init__.pyi', 'webdriver/support/color.pyi', 'webdriver/support/ui.pyi', 'webdriver/support/event_firing_webdriver.pyi', 'webdriver/support/expected_conditions.pyi', 'webdriver/support/events.pyi', 'webdriver/support/wait.pyi', 'webdriver/support/abstract_event_listener.pyi', 'webdriver/common/action_chains.pyi', 'webdriver/common/keys.pyi', 'webdriver/common/__init__.pyi', 'webdriver/common/alert.pyi', 'webdriver/common/proxy.pyi', 'webdriver/common/desired_capabilities.pyi', 'webdriver/common/utils.pyi', 'webdriver/common/touch_actions.pyi', 'webdriver/common/by.pyi', 'webdriver/common/service.pyi', 'webdriver/common/actions/__init__.pyi', 'webdriver/common/actions/key_input.pyi', 'webdriver/common/actions/pointer_input.pyi', 'webdriver/common/actions/action_builder.pyi', 'webdriver/common/actions/key_actions.pyi', 'webdriver/common/actions/mouse_button.pyi', 'webdriver/common/actions/input_device.pyi', 'webdriver/common/actions/interaction.pyi', 'webdriver/common/actions/pointer_actions.pyi', 'webdriver/common/html5/__init__.pyi', 'webdriver/common/html5/application_cache.pyi', 'webdriver/phantomjs/__init__.pyi', 'webdriver/phantomjs/webdriver.pyi', 'webdriver/phantomjs/service.pyi', 'webdriver/opera/__init__.pyi', 'webdriver/opera/options.pyi', 'webdriver/opera/webdriver.pyi', 'webdriver/ie/__init__.pyi', 'webdriver/ie/options.pyi', 'webdriver/ie/webdriver.pyi', 'webdriver/ie/service.pyi', 'webdriver/firefox/extension_connection.pyi', 'webdriver/firefox/__init__.pyi', 'webdriver/firefox/options.pyi', 'webdriver/firefox/firefox_profile.pyi', 'webdriver/firefox/webelement.pyi', 'webdriver/firefox/remote_connection.pyi', 'webdriver/firefox/webdriver.pyi', 'webdriver/firefox/firefox_binary.pyi', 'webdriver/firefox/service.pyi', 'webdriver/webkitgtk/__init__.pyi', 'webdriver/webkitgtk/options.pyi', 'webdriver/webkitgtk/webdriver.pyi', 'webdriver/webkitgtk/service.pyi', 'webdriver/edge/__init__.pyi', 'webdriver/edge/options.pyi', 'webdriver/edge/webdriver.pyi', 'webdriver/edge/service.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
