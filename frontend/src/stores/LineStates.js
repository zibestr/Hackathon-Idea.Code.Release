import { defineStore } from "pinia";

export const LineStore = defineStore('lines_store', {
  state: () => ({
    reg_line: {
      reg_second_line: false,
      reg_third_line: false
    },
    auth_line: {
      auth_second_line: false
    }
  }),
  actions: {
    change_value(name, value) {
      if (name in this.reg_line) {
        this.reg_line[name] = value;
      }
    },
    change_auth_value(value) {
      this.auth_line.auth_second_line = value;
    }
  },
  persist: {
    paths: ['reg_line']
  }
});