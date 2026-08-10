#!/bin/bash
# Check systemd status for hermes services
systemctl is-active --quiet hermes-default.service || systemctl restart hermes-default.service
