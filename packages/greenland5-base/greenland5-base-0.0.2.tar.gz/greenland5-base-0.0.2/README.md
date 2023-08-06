# Greenland5 Base Package
## About

'greenland5-base' provides foundational features that need to be
available to every Greenland5 package and interfaces (hooks) into
installed Greenland5 packages. Currently this is mostly a commandline
interface - 'greenland' - that allows to execute the built-in self
tests via 'greenland bist'.

## Future Plans

- Factor out runtime for commandline interfaces (mainly the subcommand
  registry) and make it available via the (future) 'greenland.cmdline'
  package. See Stories/cmdline-runtime-exposed.org.

