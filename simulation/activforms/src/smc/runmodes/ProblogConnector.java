package problog;

import mapek.AdaptationOption;
import mapek.Configuration;
import mapek.Environment;
import smc.runmodes.SMCConnector;
import sun.reflect.generics.reflectiveObjects.NotImplementedException;

import java.util.List;

public class ProblogConnector extends SMCConnector {


    List<AdaptationOption> adaptationOptions;
    Configuration configuration;
    Environment environment;


    public ProblogConnector() {

    }


    public void setAdaptationOptions(List<AdaptationOption> adaptationOptions, Configuration configuration) {
        this.adaptationOptions = adaptationOptions;
        this.configuration = configuration;
        this.environment = configuration.environment;
    }

    public void verify() {
        AdaptationOption option = adaptationOptions.get(0);
        System.out.println(option.toPrologString());

        throw new NotImplementedException();
    }

    @Override
    public void startVerification() {
        
    }
}
