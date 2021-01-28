export default class ConfigFetcher {
  intialize() {
    this.cachedConfig = null;
  }
  
  async fetch() {
    if (this.cachedConfig) return this.cachedConfig;
    
    const config = await (await fetch('./config')).json();
    this.cachedConfig = config;
    return config;
  }
}
