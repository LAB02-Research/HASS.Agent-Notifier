# HASS.Agent Notifier

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

This <a href="https://www.home-assistant.io" target="_blank">Home Assistant</a> integration allows you to send notifications to <a href="https://github.com/LAB02-Research/HASS.Agent" target="_blank">HASS.Agent</a>, a Windows-based Home Assistant client.

Note: it won't be of much use if you don't have HASS.Agent installed & configured on at least one device.

Contents
========

 * [Functionality](#functionality)
 * [Installation](#installation)
 * [Configuration](#configuration)
 * [Usage](#usage)
 * [Wishlist](#wishlist)

Functionality
---

Currently, it's possible to send normal (text-based) and image notifications. 


Installation
---

The easiest way to install is to use <a href="https://hacs.xyz" target="_blank">HACS</a>. Simply search for **HASS.Agent Notifier**, install and restart Home Assistant.

If you want to manually install, copy the `hass.agent notifier` folder into the `config\custom_components` folder of your Home Assistant instance, and restart.


Configuration
---

This integration exposes itself as a <a href="https://www.home-assistant.io/integrations/notify/" target="_blank">notifications integration</a>, and has to be configured as such:

```yaml
notify: 
  name: "hass agent test device"
  platform: hass_agent_notifier
  resource: http://{device_ip}:5115/notify
```

Replace `{device_ip}` with the IP of the device that has an HASS.Agent instance running. Optionally replace `5115` if you've configured a different port.

Restart Home Assistant to load your configuration.


Usage
---

### General

Currently, there are four variables you can set:

 * `message`: the message you want to show
 * `title`: the title of your popup [optional]
 * `image`: http(s) url containing the location of an image [optional]
 * `duration`: duration (in seconds) for which the popup will be shown [optional]

### Text notification

```yaml
  action:
    - service: notify.hass_agent_test_device
      data:
        message: "This is a test message."
```

### Text notification with title and duration

```yaml
  action:
    - service: notify.hass_agent_test_device
      data:
        message: "This is a test message with title and 3 sec duration."
        title: "HASS.Agent Test"
        data:
          duration: 3
```

### Image notification

```yaml
  action:
    - service: notify.hass_agent_test_device
      data:
        message: "This is a test message with an image."
        data:
          image: "http://10.0.0.6:1234/jpeg/image.jpg"
```


Wishlist
---

List of things I want to add somewhere down the road:

 * ability to add commands
 * add 'critical' type to attract more attention

If you have any other wishes, feel free to submit a ticket.
