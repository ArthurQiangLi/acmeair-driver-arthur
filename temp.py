def plot_all_data_in_sub_window():
    # Generate the subplots
    num_metrics = len(metrics) + 1  # <-- Include 'total_utility' as an additional metric
    rows, cols = 4, 2  # Set up a 3x2 grid for subplots
    fig, axs = plt.subplots(rows, cols, figsize=(15, 10))  # Create a figure with subplots
    fig.suptitle("Metrics Over Time", fontsize=16)

    # Plot each metric in a separate subplot, including 'total_utility'
    print("Generating plots...")
    for idx, metric in enumerate(metrics + [{"id": "total_utility"}]):  # <-- Added 'total_utility'
        metric_id = metric['id']
        row = idx // cols
        col = idx % cols
        ax = axs[row, col]  # Get the correct subplot

        # Plot the metric on its subplot, if the data is present in the DataFrame
        if metric_id in df.columns:
            ax.plot(df['Timestamp'], df[metric_id], marker='o')
            ax.set_title(f"{metric_id}")
            ax.set_xlabel('Time')
            
            # Assign y-axis labels based on the metric ID
            if metric_id == 'memory.limit.used.percent':
                ax.set_ylabel('Memory Limit Used (%)')
            elif metric_id == 'net.http.request.time':
                ax.set_ylabel('Net Request Time (ms)')
                ax.set_ylim(0, 600)
            elif metric_id == 'cpu.quota.used.percent':
                ax.set_ylabel('CPU Quota Used (%)')
            elif metric_id == 'net.http.request.time.worst':
                ax.set_ylabel('Net Request Time Worst(ms)')
                ax.set_ylim(0, 600)
            elif metric_id == 'total_utility':
                ax.set_ylabel('Total Utility')
                ax.set_ylim(0, 1.1)  # Set y-axis range for utility score
            elif metric_id == 'cpu.used.percent':
                ax.set_ylabel('CPU Used (%)')
            else:
                ax.set_ylabel(metric_id)
            ax.grid(True)
            ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for readability

    # Hide any unused subplots
    for idx in range(num_metrics, rows * cols):
        fig.delaxes(axs.flatten()[idx])

    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to fit title
    plot_filename = os.path.join(output_dir, "combined_metrics_plot_subs.png")
    plt.savefig(plot_filename)
    plt.show()
