#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

class atopStore(object):

  restkey = "unknown"
  
  restval = None

  skip_fieldnames = [restkey, "label", "host", "date", "time"]

  __common_fieldnames = ["label", "host", "epoch", "date", "time", "interval"]

  CPU_fieldnames = __common_fieldnames + ["ticks_per_second", "number_of_processors", "system", "user", "nice", "idle", "wait", "irq", "sirq", "steal", "guest"]

  cpu_fieldnames = __common_fieldnames + ["ticks_per_second", "processor_number", "system", "user", "nice", "idle", "wait", "irq", "sirq", "steal", "guest"]

  CPL_fieldnames = __common_fieldnames + ["number_of_processors", "last_minute", "last_five_minutes", "last_fifteen_minutes", "number_of_context_switches", "number_of_interrupts"]

  MEM_fieldnames = __common_fieldnames + ["page_size", "size_of_physical_memory", "size_of_free_memory", "size_of_page_cache", "size_of_buffer_cache", "size_of_slab", "number_of_dirty_pages"]

  SWP_fieldnames = __common_fieldnames + ["page_size", "size_of_swap", "size_of_free_swap", "0", "size_of_committed_space", "limit_for_committed_space"]

  PAG_fieldnames = __common_fieldnames + ["page_size", "number_of_page_scans", "number_of_allocstalls", "0", "number_of_swapins", "number_of_swapouts"]

  LVM_fieldnames = __common_fieldnames + ["name", "number_of_milliseconds_spent_for_I/O", "number_of_reads_issued", "number_of_sectors_transferred_for_reads", "number_of_writes_issued", "number_of_sectors_transferred_for_write"]

  MDD_fieldnames = LVM_fieldnames
  
  DSK_fieldnames = LVM_fieldnames
  
  NET_fieldnames = __common_fieldnames + ["name", "number_of_packets_received", "number_of_bytes_received", "number_of_packets_transmitted", "number_of_bytes_transmitted", "speed", "duplex_mode"]

  def __init__(self, filename, delimiter=' '):
    self.filename = filename
    self.delimiter = delimiter

  def __getattr__(self, name):
    func = name.split('_')
    if "fetch" != func[0] or 2 != len(func):
      return object.__getattribute__(self, name)

    def method(*args):
      items = []
      ret = {}
      for data in self.iter_label(func[1]):
        for key in data.keys():
          if self.restkey == key or key in self.skip_fieldnames:
            continue
          try:
            exec key in locals()
          except NameError:
            cmd = key + "=[]"
            items.append(key)
            #print cmd
            exec cmd in locals()
          cmd = key + ".append(" + data[key] + ")"
          #print cmd
          exec cmd in locals()
      for item in items:
        cmd = "ret['" + item + "']=" + item
        #print cmd
        exec cmd in locals()
      #print locals()
      return ret
    return method

  def iter_label(self, label):
    csvfile = open(self.filename, "r")
    fields = atopStore.__dict__[label + "_fieldnames"]
    r = csv.DictReader(csvfile, fieldnames=fields, restkey=atopStore.restkey, restval=atopStore.restval, delimiter=self.delimiter)
    for line in r:
      if line and line["label"] == label:
        yield line

if __name__ == "__main__":
  store = atopStore("20120709ALL.txt")
  a = store.fetch_cpu()
  print a

