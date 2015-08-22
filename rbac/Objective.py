Objective instproc addDerivedAbstractContextCondition {condition} {
  my instvar derived_conditions
  if {[info exists derived_conditions]} {
    if {[lsearch -exact $derived_conditions $condition] == -1} {
      lappend derived_conditions $condition
      my log NORMAL "[self] [self proc], abstract context condition <<$condition>>\
                         added to <<derived_conditions>> list."
      return 1
    } else {
      my log FAILED "[self] [self proc] FAILED, abstract condition <<$condition>>\
                         is already in the <<derived_conditions>> list."
      return 0
    }
  } else {
    lappend derived_conditions $condition
    my log NORMAL "[self] [self proc], abstract context condition <<$condition>>\
                       added to <<derived_conditions>> list."
    return 1
  }
}

Objective instproc removeDerivedAbstractContextCondition {condition} {
  my instvar derived_conditions
  if {[info exists derived_conditions]} {
    set index [lsearch -exact $derived_conditions $condition]
    if {$index != -1} {
      set derived_conditions [lreplace $derived_conditions $index $index]
      my log NORMAL "[self] [self proc], abstract context condition <<$condition>>\
                         removed from <<derived_conditions>> list."
      return 1
    } else {
      my log FAILED "[self] [self proc] FAILED, abstract context condition\
                         <<$condition>> is not in <<derived_conditions>> list."
      return 0
    }
  } else {
    my log FAILED "[self] [self proc] FAILED, abstract context condition <<$condition>>\
                       is not in <<derived_conditions>> list."
    return 0
  }
}

Objective instproc clearDerivedConditionList {} {
  my instvar derived_conditions
  if {[info exists derived_conditions]} {
    unset derived_conditions
  }
  return 1
}

Objective instproc getDerivedConditionList {} {
  my instvar derived_conditions
  if {[info exists derived_conditions]} {
    return $derived_conditions
  } else {
    return ""
  }
}
