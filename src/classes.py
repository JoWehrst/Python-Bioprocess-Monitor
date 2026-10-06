import os

# Imports libraries needed to make graphs and load CSV files
import pandas as pd
import matplotlib.pyplot as plt


# This stores a dataset and operator limits
class BioprocessMonitor:
    def __init__(self, filepath, ph_lims, temperature_lims):
        print("========================  IMPORT FERMENTATION DATA SET  =======================")
        print("Loading...")

        # Imports desired dataset
        print(f"Dataset taken: {filepath}")
        self.data = pd.read_csv(filepath)

        # Stores operating ranges for future reference
        self.ph_lims = ph_lims
        self.temperature_lims = temperature_lims

        # Informs operator if data was successfully imported
        print("\n Dataset has been successfully imported.")
        print(f"# of Measurements: {len(self.data)}")
        print(f"# of Batches: {self.get_n_batches()}")
        print("\n                               TASK COMPLETED                               \n")

    def extract_batch(self, batch_id):
        print("=======================  NOW EXTRACTING TO SINGLE BATCH  ======================")
        print("Loading...")

        # Extracts the selected batch from the dataset
        df_batch = self.data.loc[self.data.loc[:, "batch_id"] == batch_id]

        print("\n                               TASK COMPLETED                               \n")

        return df_batch

    def get_n_batches(self):
        print("=============  CHECKING NUMBER OF UNIQUE BATCHES PRESENT IN DATA  =============")
        print("Loading...")

        # Counts the number of unique batches
        n_batches = self.data.loc[:, "batch_id"].nunique()

        print("\n                               TASK COMPLETED                               \n")

        return n_batches

    def export_dashboard(self, batch_id, filepath):
        print("======================  SAVING FIGURES FOR DASH BOARD  =======================")
        print("Loading...")

        # Extract and sort batch data selected
        df_batch = self.extract_batch(batch_id)
        df_batch = df_batch.sort_values("time_h")

        # Defines colours and markers for the graphs
        COLORS = ["tab:blue", "tab:green", "tab:purple", "tab:red"]
        MARKERS = ["o", "s", "^", "X"]

        # Creates the 2 x 2 dashboard
        fig, axes = plt.subplots(
            2, 2,
            figsize=(10, 10),
            dpi=200,
            layout="constrained"
        )

        # ============================================================
        # Concentration graph
        # ============================================================

        ax = axes[0, 0]

        # Plots glucose concentration
        ax.scatter(
            df_batch.loc[:, "time_h"],
            df_batch.loc[:, "C_glucose_g_L^-1"],
            color=COLORS[0],
            marker=MARKERS[0],
            s=32,
            label="Glucose"
        )

        # Plots biomass concentration
        ax.scatter(
            df_batch.loc[:, "time_h"],
            df_batch.loc[:, "C_biomass_g_L^-1"],
            color=COLORS[1],
            marker=MARKERS[1],
            s=32,
            label="Biomass"
        )

        # Plots product concentration
        ax.scatter(
            df_batch.loc[:, "time_h"],
            df_batch.loc[:, "C_product_g_L^-1"],
            color=COLORS[2],
            marker=MARKERS[2],
            s=32,
            label="Product"
        )

        ax.set_xlabel("Time [h]", fontsize=10)
        ax.set_ylabel("Concentration [g/L]", fontsize=10)

        ax.tick_params(axis="both", which="major", labelsize=10)

        ax.legend(fontsize=9)

        # ============================================================
        # Temperature graph
        # ============================================================

        ax = axes[0, 1]

        # Creates empty lists for the two temperature groups
        optimal_time = []
        optimal_temperature = []

        outside_time = []
        outside_temperature = []

        # Checks each temperature measurement
        for i in range(len(df_batch)):

            time = df_batch["time_h"].iloc[i]
            temperature = df_batch["temperature_C"].iloc[i]

            if temperature >= self.temperature_lims[0] and temperature <= self.temperature_lims[1]:

                # Temperature is within the acceptable range
                optimal_time.append(time)
                optimal_temperature.append(temperature)

            else:

                # Temperature is outside the acceptable range
                outside_time.append(time)
                outside_temperature.append(temperature)

        # Plots temperatures within the acceptable range
        ax.scatter(
            optimal_time,
            optimal_temperature,
            color=COLORS[1],
            marker=MARKERS[0],
            s=32,
            label="Optimal"
        )

        # Plots temperatures outside the acceptable range
        ax.scatter(
            outside_time,
            outside_temperature,
            color=COLORS[3],
            marker=MARKERS[3],
            s=32,
            label="Outside range"
        )

        ax.set_xlabel("Time [h]", fontsize=10)
        ax.set_ylabel("Temperature [°C]", fontsize=10)

        ax.tick_params(axis="both", which="major", labelsize=10)

        ax.legend(fontsize=9)

        # ============================================================
        # pH graph
        # ============================================================

        ax = axes[1, 0]

        # Creates empty lists for the two pH groups
        optimal_time = []
        optimal_ph = []

        outside_time = []
        outside_ph = []

        # Checks each pH measurement
        for i in range(len(df_batch)):

            time = df_batch["time_h"].iloc[i]
            ph = df_batch["pH"].iloc[i]

            if ph >= self.ph_lims[0] and ph <= self.ph_lims[1]:

                # pH is within the acceptable range
                optimal_time.append(time)
                optimal_ph.append(ph)

            else:

                # pH is outside the acceptable range
                outside_time.append(time)
                outside_ph.append(ph)

        # Plots pH values within the acceptable range
        ax.scatter(
            optimal_time,
            optimal_ph,
            color=COLORS[1],
            marker=MARKERS[0],
            s=32,
            label="Optimal"
        )

        # Plots pH values outside the acceptable range
        ax.scatter(
            outside_time,
            outside_ph,
            color=COLORS[3],
            marker=MARKERS[3],
            s=32,
            label="Outside range"
        )

        ax.set_xlabel("Time [h]", fontsize=10)
        ax.set_ylabel("pH", fontsize=10)

        ax.tick_params(axis="both", which="major", labelsize=10)

        ax.legend(fontsize=9)

        # ============================================================
        # Dissolved oxygen graph
        # ============================================================

        ax = axes[1, 1]

        ax.scatter(
            df_batch.loc[:, "time_h"],
            df_batch.loc[:, "DO_percent"],
            color=COLORS[0],
            marker=MARKERS[0],
            s=32,
            label="Dissolved oxygen"
        )

        ax.set_xlabel("Time [h]", fontsize=10)
        ax.set_ylabel("Dissolved oxygen [%]", fontsize=10)

        ax.tick_params(axis="both", which="major", labelsize=10)

        ax.legend(fontsize=9)

        # Adds a title to the entire dashboard
        fig.suptitle(
            f"Bioprocess Dashboard - Batch {batch_id}",
            fontsize=12
        )

        # Creates the output folder if necessary
        output_folder = os.path.dirname(filepath)

        if output_folder:
            os.makedirs(output_folder, exist_ok=True)

        # Saves the figure
        fig.savefig(filepath)

        print(f"\nDashboard saved: {filepath}")

        # Closes the figure
        plt.close(fig)

        print("\n                               TASK COMPLETED                               ")
        print("                               DASHBOARD COMPLETED!                         \n")

    def export_summary(self, filepath):
        print("=======================  GENERATE BATCH SUMMARY TABLE  =========================")
        print("Loading...")

        summary = []

        # Fetches all unique batch IDs
        batch_ids = self.data.loc[:, "batch_id"].dropna().unique()

        # Calculates the summary for each batch
        for batch_id in batch_ids:

            df_batch = self.extract_batch(batch_id)
            df_batch = df_batch.sort_values("time_h")

            # ========================================================
            # Calculate percentage of measurements with optimal pH
            # ========================================================

            ph_optimal_count = 0

            for i in range(len(df_batch)):

                ph = df_batch["pH"].iloc[i]

                if ph >= self.ph_lims[0] and ph <= self.ph_lims[1]:
                    ph_optimal_count += 1

                else:
                    pass

            ph_optimal_percent = (
                ph_optimal_count / len(df_batch) * 100
            )

            # ========================================================
            # Calculate percentage of measurements with optimal
            # temperature
            # ========================================================

            temperature_optimal_count = 0

            for i in range(len(df_batch)):

                temperature = df_batch["temperature_C"].iloc[i]

                if temperature >= self.temperature_lims[0] and temperature <= self.temperature_lims[1]:
                    temperature_optimal_count += 1

                else:
                    pass

            temperature_optimal_percent = (
                temperature_optimal_count / len(df_batch) * 100
            )

            # ========================================================
            # Find final product concentration
            # ========================================================

            final_products = (
                df_batch.loc[
                    df_batch.index[-1],
                    "C_product_g_L^-1"
                ]
            )

            # Adds the batch results to the summary
            summary.append({
                "batch_id": batch_id,
                "ph_optimal_percent": round(ph_optimal_percent, 2),
                "temperature_optimal_percent": round(
                    temperature_optimal_percent, 2
                ),
                "C_product_g_L^-1_final": final_products
            })

        # Creates the summary DataFrame
        summary_df = pd.DataFrame(summary)

        # Creates the output folder if necessary
        output_folder = os.path.dirname(filepath)

        if output_folder:
            os.makedirs(output_folder, exist_ok=True)

        # Exports the summary
        summary_df.to_csv(filepath, index=False)

        print("\n                              TASK COMPLETED                               ")
        print("                               TABLES COMPLETED!                           \n")
        print("============================ ALL TASKS COMPLETED! ===========================")
        print("=============================================================================")