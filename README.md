[![Validate](https://github.com/LAB02-Research/HASS.Agent-Notifier/workflows/Validate/badge.svg)](https://github.com/LAB02-Research/HASS.Agent-Notifier/actions?query=workflow:"Validate")
[![GitHub release](https://img.shields.io/github/release/LAB02-Research/HASS.Agent-Notifier?include_prereleases=&sort=semver&color=blue)](https://github.com/LAB02-Research/HASS.Agent-Notifier/releases/)
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)


# HASS.Agent Notifier

This <a href="https://www.home-assistant.io" target="_blank">Home Assistant</a> integration allows you to send notifications to <a href="https://github.com/LAB02-Research/HASS.Agent" target="_blank">HASS.Agent</a>, a Windows-based Home Assistant client.

Note: it won't be of much use if you don't have HASS.Agent installed & configured on at least one PC (or Windows based device).

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/lab02research)

----

### Contents

 * [Functionality](#functionality)
 * [Installation](#installation)
 * [Configuration](#configuration)
 * [Debugging](#debugging)
 * [Installation and Configuration Summary](#installation-and-configuration-summary)
 * [Usage](#usage)
 * [Wishlist](#wishlist)
 * [License](#license)

----

### Functionality

Currently, it's possible to send normal (text-based) and image notifications. 

----

### Installation

The easiest way to install is to use <a href="https://hacs.xyz" target="_blank">HACS</a>. Simply search for **HASS.Agent Notifier**, install and restart Home Assistant.

If you want to manually install, copy the `hass_agent_notifier` folder into the `config\custom_components` folder of your Home Assistant instance, and restart.

----

### Configuration

This integration exposes itself as a <a href="https://www.home-assistant.io/integrations/notify/" target="_blank">notifications integration</a>, and has to be configured as such:

```yaml
notify: 
  name: "hass agent test device"
  platform: hass_agent_notifier
  resource: http://{device_ip}:5115/notify
```

Replace `{device_ip}` with the IP of the device that has an HASS.Agent instance running. To find your IP, run `ipconfig` in a command prompt on your PC. Look for the value after `IPv4 Address`. Optionally replace `5115` if you've configured a different port, normally you shouldn't have to.

Restart Home Assistant to load your configuration.

The port needs to be open on the target device. HASS.Agent will offer to do this for you during the onboarding process. 
To do so manually, you can run this command in an elevated prompt:

`netsh advfirewall firewall add rule name="HASS.Agent Notifier" dir=in action=allow protocol=TCP localport=5115`

----

### Debugging

If something's not working as it should, while everything's configured and HASS.Agent isn't showing any errors in its logs, browse to the following URL from another PC on the same network as HASS.Agent: `http://{hass_agent_ip}:5115`. Make sure to change `{hass_agent_ip}` to the IP of the PC where HASS.Agent's installed.

If HASS.Agent is configured and the firewall rule's active, you'll see: `HASS.Agent Active`. 

If not, something is blocking access to HASS.Agent. Add the following snippet to your configuration.yaml to enable debug logging for the integration:


```yaml
logger:
  default: warning
  logs:
    custom_components.hass_agent_notifier: debug
```

Reboot Home Assistant. Whenever you send a message, this should show up in your logs:

![Debug Output](https://raw.githubusercontent.com/LAB02-Research/HASS.Agent/main/Images/notifier_debug_logging.png)

If not, please open a ticket a post your log output.

----

### Installation and Configuration Summary

Quick summary to get things working:

- Install **HASS.Agent-Notifier** integration, either through HACS or manually
- Reboot Home Assistant
- Create a `notify` entity, make sure you enter the right IP for your PC
- Reboot Home Assistant
- Start adding the new entity to your automations & scripts :)

----

### Usage

#### General

Currently, there are four variables you can set:

 * `message`: the message you want to show
 * `title`: the title of your popup [optional]
 * `image`: http(s) url containing the location of an image [optional]
 * `duration`: duration (in seconds) for which the popup will be shown [optional]

#### Text notification

```yaml
  action:
    - service: notify.hass_agent_test_device
      data:
        message: "This is a test message."
```

#### Text notification with title and duration

```yaml
  action:
    - service: notify.hass_agent_test_device
      data:
        message: "This is a test message with title and 3 sec duration."
        title: "HASS.Agent Test"
        data:
          duration: 3
```

#### Image notification

```yaml
  action:
    - service: notify.hass_agent_test_device
      data:
        message: "This is a test message with an image."
        data:
          image: "http://10.0.0.6:1234/jpeg/image.jpg"
```

#### Script GUI examples

This is the sequence part of a test script to send a text-only message, created through the Home Assistant GUI:

![Script Test Notification](https://raw.githubusercontent.com/LAB02-Research/HASS.Agent/main/Images/notifier_script_example.png)

This is the same script, but with an image added to the notification:

![Script Test Image Notification](https://raw.githubusercontent.com/LAB02-Research/HASS.Agent/main/Images/notifier_script_image_example.png)

You can use the new <a href="https://www.home-assistant.io/lovelace/button/" target="_blank">Button Card</a> to trigger your test scripts.

----

### Wishlist

List of things I want to add somewhere down the road:

 * ability to add commands
 * add 'critical' type to attract more attention
 * show a videostream for x seconds with size y (small/normal/fullscreen) on position z (bottom right, center screen, etc)

If you have any other wishes, feel free to submit a ticket.

----

### License

HASS.Agent Notifier and HASS.Agent are released under the <a href="https://opensource.org/licenses/MIT" target="_blank">MIT license</a>.
