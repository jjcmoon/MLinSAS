package mapek;

public class Qualities {
	public double packetLoss;
	public double energyConsumption;
	public double latency;

	public Qualities getCopy() {
		Qualities qualities = new Qualities();
		qualities.packetLoss = this.packetLoss;
		qualities.energyConsumption = this.energyConsumption;
		qualities.latency = this.energyConsumption;
		return qualities;
	}

	public String toString() {
		return Double.toString(packetLoss) + ";" + Double.toString(latency) + ";" + Double.toString(energyConsumption);
	}
}
