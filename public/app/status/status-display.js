import wait from '../lib/wait.js';

export default class StatusDisplay {
  constructor({ el }) {
    this.el = el;
    this.template = this.el.querySelector('#status_template');
    this.content = this.el.querySelector('#status_content');
  }

  async fetchData() {
    this.data = await (await fetch('/status')).json();
  }
  
  createContentFragment() {
    const { moisture, state } = this.data;
    const content = this.template.content.cloneNode(true);
    const img = content.querySelector('img');
    img.setAttribute('src', img.getAttribute('src').replace('[state]', state));
    const moistureEl = content.querySelector('#moisture');
    moistureEl.innerHTML = moistureEl.innerHTML.replace('[moisture]', moisture);
    return content;
  }

  async update() {
    this.content.innerHTML = '';
    this.content.appendChild(this.createContentFragment());
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
