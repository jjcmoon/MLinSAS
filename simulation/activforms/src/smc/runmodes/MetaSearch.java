
package smc.runmodes;

import java.util.HashMap;

import mapek.AdaptationOption;
import mapek.Environment;
import mapek.Link;
import mapek.Mote;
import mapek.SNR;
import mapek.TrafficProbability;
import util.Pair;


public class MetaSearch extends SMCConnector {


    public MetaSearch() {}

    @Override
	public void startVerification() {
		System.out.print(";" + adaptationOptions.size());

	}


	private AdaptationOption naiveOptimizer(AdaptationOption option) {
	    // Reset distributions

        option.system.getMotes().stream()
                .map(mote -> mote.getLinks())
                .flatMap(links -> links.stream())
                .forEach(link -> link.setDistribution(0));

		HashMap<Integer, Pair<Integer, Double>> motePL = new HashMap();
		motePL.put(1, new Pair(0, 0.0));
		boolean changed = true;
		Double x, y, t;
		while (changed) {
			changed = false;
			for (Mote mote : configuration.system.getMotes()) {
			    for (Link link : mote.getLinks()) {
                    if (motePL.containsKey(link.destination)) {
                        Pair<Integer, Double> re = motePL.get(link.destination);
                        x = re.second;
                        y = SNRtoPL(environment.getSNR(link));
                        t = 1 - (1-x)*(1-y);
                        if (motePL.getOrDefault(link.source,new Pair<>(0,Double.POSITIVE_INFINITY)).second > t) {
                            changed = true;
                            motePL.put(link.source, new Pair<>(link.destination, t));
                        }

                    }
                }
			}
		}

		for (int i : motePL.keySet()) {
		    int j = motePL.get(i).first;
		    option.system.getMote(i).getLink(j).setDistribution(100);
        }

		return option;

	}



    private static Double SNRtoPL(Double SNR) {
        return clamp(-SNR / 40, 0.0, 1.0);
    }

    private static Double clamp(Double a, Double lower, Double upper) {
	    if (a < lower)
	        return lower;
	    if (a > upper)
	        return upper;
	    return a;
    }




}
