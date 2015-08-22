


Permission instproc getContextConstraints {} {
  my instvar contextconstraints
  if {[info exists contextconstraints]} {
    return $contextconstraints
  } 
  return ""
}
