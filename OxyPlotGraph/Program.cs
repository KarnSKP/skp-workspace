using System;
using OxyPlot;
using OxyPlot.Series;
using OxyPlot.ImageSharp;

class Program
{
    static void Main(string[] args)
    {
        // Create a PlotModel
        var plotModel = new PlotModel { Title = "Line Graph Example" };

        // Create a LineSeries
        var lineSeries = new LineSeries
        {
            Title = "Data Points",
            MarkerType = MarkerType.Circle
        };

        // Add data points to the LineSeries
        lineSeries.Points.Add(new DataPoint(0, 0));
        lineSeries.Points.Add(new DataPoint(1, 2));
        lineSeries.Points.Add(new DataPoint(2, 4));
        lineSeries.Points.Add(new DataPoint(3, 8));

        // Add the LineSeries to the PlotModel
        plotModel.Series.Add(lineSeries);

        // Export the plot as an image
        var jpegExporter = new JpegExporter(600, 400, 96); // Width, Height, Resolution
        using (var stream = System.IO.File.Create("plot.jpeg"))
        {
            jpegExporter.Export(plotModel, stream);
        }

        Console.WriteLine("Plot saved as plot.jpeg");
    }
}
