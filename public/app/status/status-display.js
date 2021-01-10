import wait from '../lib/wait.js';

export default class StatusDisplay {
  constructor({ el }) {
    this.el = el;
  }

  async fetchData() {
    this.data = await (await fetch('/status')).json();
  }

  async update() {
    const { moisture, state } = this.data;
    this.el.innerHTML = `moisture: ${moisture}, state: ${state}`;
  }

  async fetchAndUpdate() {
    await this.fetchData();
    this.update();
  }
  
  async updateLoop() {
    await Promise.all([this.fetchAndUpdate(), wait(5000)]);
    setTimeout(() => this.updateLoop(), 0);
  }

  attach() {
    this.updateLoop();
  }
}
