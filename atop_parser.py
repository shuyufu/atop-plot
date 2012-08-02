#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

class atopStore(object):

  __common_fieldnames = ["label", "host", "epoch", "date", "time", "interval"]

  CPU_fieldnames = __common_fieldnames + ["ticks_per_second", "number_of_processors", "system", "user", "nice", "idle", "wait", "irq", "sirq", "steal", "guest", "unknown1", "unknown2"]

  cpu_fieldnames = __common_fieldnames + ["ticks_per_second", "processor_number", "system", "user", "nice", "idle", "wait", "irq", "sirq", "steal", "guest", "unknown1", "unknown2"]

  CPL_fieldnames = __common_fieldnames + ["number_of_processors", "last_minute", "last_five_minutes", "last_fifteen_minutes", "number_of_context_switches", "number_of_interrupts"]

  MEM_fieldnames = __common_fieldnames + ["page_size", "size_of_physical_memory", "size_of_free_memory", "size_of_page_cache", "size_of_buffer_cache", "size_of_slab", "number_of_dirty_pages"]

  SWP_fieldnames = __common_fieldnames + ["page_size", "size_of_swap", "size_of_free_swap", "0", "size_of_committed_space", "limit_for_committed_space"]

  PAG_fieldnames = __common_fieldnames + ["page_size", "number_of_page_scans", "number_of_allocstalls", "0", "number_of_swapins", "number_of_swapouts"]

  LVM_fieldnames = __common_fieldnames + ["name", "number_of_milliseconds_spent_for_I/O", "number_of_reads_issued", "number_of_sectors_transferred_for_reads", "number_of_writes_issued", "number_of_sectors_transferred_for_write"]

  MDD_fieldnames = LVM_fieldnames

  DSK_fieldnames = LVM_fieldnames

  NET_upper_fieldnames = __common_fieldnames + ["name", "number_of_packets_received_by_TCP", "number_of_packets_transmitted_by_TCP", "number_of_packets_received_by_UDP", "number_of_packets_transmitted_by_UDP", "number_of_packets_received_by_IP", "number_of_packets_transmitted_by_IP", "number_of_packets_delivered", "number_of_packets_forwarded"]

  NET_fieldnames = __common_fieldnames + ["name", "number_of_packets_received", "number_of_bytes_received", "number_of_packets_transmitted", "number_of_bytes_transmitted", "speed", "duplex_mode"]

  def __init__(self, filename, delimiter=' '):
    self.filename = filename
    self.delimiter = delimiter

  def __getattr__(self, attr_name):
    func = attr_name.split('_')
    if "series" != func[0] or 2 != len(func):
      return object.__getattribute__(self, attr_name)

    names = {}
    items = {}

    data = csv.reader(open(self.filename, "r"), delimiter=self.delimiter)
    for row in data:
      label = row[0]
      if "SEP" == label or "RESET" == label or func[1] != label:
        continue

      if label in ["LVM", "MDD", "DSK", "NET"]:
        if row[6] not in names:
          names[row[6]] = {}
          items = names
        container = names[row[6]]
        field_index = 7
      elif label in ["cpu"]:
        if row[7] not in names:
          names[row[7]] = {}
          items = names
        container = names[row[7]]
        field_index = 8
      else:
        container = items
        field_index = 6

      if "NET" == label:
        dev = row[6]
        if "upper" == dev:
          fields = atopStore.__dict__["NET_upper_fieldnames"]
        else:
          fields = atopStore.__dict__["NET_fieldnames"]
      else:
        fields = atopStore.__dict__[label + "_fieldnames"]

      for i in [2] + range(field_index, len(row)):
        key = fields[i]
        if key not in container:
          container[key] = []
        series = container[key]
        series.append(row[i])
    return items

if __name__ == "__main__":
  store = atopStore("20120709ALL.txt")
  print store.series_MEM

