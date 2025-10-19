<div align="center">
  <h3>ha_pcpc</h3>
  <p>Monitor and control your PC via ping and Wake-on-LAN.</p>
</div>

<hr>

## About

**PC Power Control** is a Home Assistant custom integration that lets you monitor and control PCs using ping and Wake-on-LAN.

## Installation

### Via HACS (recommended)

1. Open HACS → Integrations → Custom Repositories.  
2. Add this repository URL (`https://github.com/siva1danil/ha_pcpc`) as type *Integration*.
3. Search for `PC Power Control` in HACS and install it.
4. Restart Home Assistant.

### Manual installation

1. Copy the `custom_components/ha_pcpc` folder into your Home Assistant custom components directory: `/config/custom_components/ha_pcpc/`.
2. Restart Home Assistant.

## Usage

Add the integration through *Settings* → *Devices & Services* → *Add Integration* → *PC Power Control*.
Provide only a MAC address to send Wake-on-LAN packets, only an IP address to monitor online status, or both for full power control and status detection.
