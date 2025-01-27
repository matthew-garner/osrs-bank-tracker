package catcat572;

import javax.inject.Inject;
import lombok.extern.slf4j.Slf4j;
import net.runelite.api.*;
import net.runelite.api.events.ItemContainerChanged;
import net.runelite.client.eventbus.Subscribe;
import net.runelite.client.plugins.Plugin;
import net.runelite.client.plugins.PluginDescriptor;
import net.runelite.client.game.ItemManager;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Objects;


@Slf4j
@PluginDescriptor(
	name = "Shows the value of bank over time"
)
public class BankTrackerPlugin extends Plugin
{
	@Inject
	private Client client;

	@Inject
	ItemManager itemManager;

	@Override
	protected void startUp() throws Exception
	{
		initailiseCsv();
	}

	@Override
	protected void shutDown() throws Exception
	{
		log.info("Example stopped!");
	}

	//bank id: 95
	//inventory id: 93
	//equipment id: 94
	@Subscribe
	public void onItemContainerChanged(ItemContainerChanged event)
	{
		ItemContainer container = event.getItemContainer();
		if (container != null)
		{
			for (Item item : container.getItems())
			{
				String itemName = itemManager.getItemComposition(item.getId()).getName();
				if (itemManager.getItemComposition(item.getId()).getName().equals("Coins"))
				{
					writeToCsv(item.getId(), itemName, item.getQuantity());
				}
				//log.info("Item id: {}", item);
				if (item.getId() != -1 && itemManager.getItemComposition(item.getId()).isTradeable())
				{
					if (!Objects.equals(itemName, "Bank filler")){
						//int itemPrice = itemManager.getItemPrice(item.getId()); //high alch price
						log.info("Item ID: {}, Item name: {}, Item quantity {}", item.getId(), itemName, item.getQuantity());
						writeToCsv(item.getId(), itemName, item.getQuantity());
					}
				}
			}
		}
	}

	private void initailiseCsv() {
		String csvFilePath = "src/main/resources/output.csv";
		try (BufferedWriter writer = new BufferedWriter(new FileWriter(csvFilePath))) {
			writer.write("Item ID,Item Name,Item Quantity");
			writer.newLine();
		} catch (IOException e) {
			log.error("Failed to write to CSV file", e);
		}
	}

	private void writeToCsv(int itemId, String itemName, int itemQuantity)
	{
		String csvFilePath = "src/main/resources/output.csv";
		try (BufferedWriter writer = new BufferedWriter(new FileWriter(csvFilePath, true))) {
			writer.write(String.format("%d,%s,%d%n", itemId, itemName, itemQuantity));
		} catch (IOException e) {
			log.error("Failed to write to CSV file", e);
		}
	}

}
