package domain;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public class DoubleRange implements Profile<Double> {

	private double min;
	private double max;
	private Map<Integer, Double> memory = new HashMap<>();
	private Random rand = new Random();
	private int avg = 5;

	public DoubleRange(Double min, Double max) {
		this.min = min;
		this.max = max;
	}

	@Override
	public Double get(int runNumber) {
		return getAvg(runNumber);
	}


	private void assertRunNumber(int runNumber) {
	    if (!memory.containsKey(runNumber)) {
	        double random = min + rand.nextDouble() * (max - min);
	        memory.put(runNumber, random);
        }
    }

	private double getAvg(int runNumber) {
		double sum = 0;
		int count = 0;
		for (int i = runNumber; i >= 0 && i > runNumber - avg; i--) {
            assertRunNumber(i);
			sum += memory.get(i);
			count++;
		}
		return sum / count;

	}
}
