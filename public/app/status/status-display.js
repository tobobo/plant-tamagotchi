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
  
  updateContent(el = this.content) {
    const { moisture, state } = this.data;
    const img = el.querySelector('img');
    const templateImg = this.template.content.querySelector('img');
    img.setAttribute('src', templateImg.getAttribute('src').replace('[state]', state));
    const moistureEl = el.querySelector('#moisture');
    const templateMoistureEl = this.template.content.querySelector('#moisture');
    moistureEl.innerHTML = templateMoistureEl.innerHTML.replace('[moisture]', moisture);
    return el;
  }

  async update() {
    if (this.hasInitializedContent) {
      this.updateContent();
    } else {
      const initialContent = this.updateContent(this.template.content.cloneNode(true));
      this.content.appendChild(initialContent);
      this.hasInitializedContent = true;
    }
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
