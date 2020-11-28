#!/usr/bin/env bash

generate_node() {
cat <<EOF
      <node name="${1}">
        <properties>
          <help>${1}_help</help>
        </properties>
        <children>
          <leafNode name="${1}_child">
            <properties>
              <help>${1}_child_help</help>
              <valueless/>
            </properties>
          </leafNode>
        </children>
      </node>
EOF
}

# Array
declare -a StringArray=(
"auto-update"
"disable-uniqreqids"
"esp-groups"
"ike-group"
"include-ipsec-conf"
"include-ipsec-secrets"
"ipsec-interfaces"
"logging"
"nat-networks"
"nat-traversal"
"options"
"profile"
"site-to-site"
)

for COMMAND in ${StringArray[@]}; do
    generate_node $COMMAND
done
