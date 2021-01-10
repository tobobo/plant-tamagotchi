import wait from '../lib/wait.js';

export default class StatusDisplay {
  constructor({ container }) {
    this.container = container;
  }

  async fetchData() {
    this.data = await (await fetch('/status')).json();
  }

  async update() {
    const { moisture, state } = this.data;
    this.container.innerHTML = `moisture: ${moisture}, state: ${state}`;
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
