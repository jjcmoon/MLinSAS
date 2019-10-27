package mapek;

import java.util.Collection;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;

import com.google.gson.Gson;

// This class holds the motes and their properties of the managed system
// The mote class keeps a list of the connected links
// which in turn contain their own properties.
public class ManagedSystem {

	public HashMap<Integer, Mote> motes = new LinkedHashMap<Integer, Mote>();

	public ManagedSystem() {

	}

	public ManagedSystem(List<Mote> motes) {
		for (Mote mote : motes) {
			this.motes.put(mote.getMoteId(), mote);
		}
	}

	public Collection<Mote> getMotes() {
		return motes.values();
	}

	public void setMote(int moteId, Mote mote) {
		motes.put(moteId, mote);
	}

	public Mote getMote(int moteId) {
		return motes.get(moteId);
	}

	public ManagedSystem getCopy() {
		ManagedSystem managedSystem = new ManagedSystem();
		for (Mote mote : motes.values()) {
			managedSystem.motes.put(mote.getMoteId(), mote.getCopy());
		}
		return managedSystem;
	}

	@Override
	public String toString() {
		return new Gson().toJson(this);
	}
}
