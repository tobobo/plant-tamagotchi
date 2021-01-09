export default class StatusDisplay {
  constructor({ container }) {
    this.container = container;
  }

  async fetchData() {
    this.data = await (await fetch('/status')).json();
  }

  async render() {
    await this.fetchData();
    const { moisture, state } = this.data;
    this.container.innerHTML = `moisture: ${moisture}, state: ${state}`
  }
}
