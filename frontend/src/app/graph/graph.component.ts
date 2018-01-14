import { Component, ElementRef, Input, ViewChild, OnInit, OnChanges, AfterViewChecked } from '@angular/core';
import * as d3 from 'd3';
import * as legend from 'd3-svg-legend'
import * as _ from 'underscore';

@Component({
  selector: 'app-graph',
  styleUrls: ['./graph.component.scss'],
  templateUrl: 'graph.component.html'
})
export class GraphComponent implements OnInit, OnChanges, AfterViewChecked {
  @ViewChild('bubbleChartContainer') private chartContainer: ElementRef;
  @Input() private data: Array<any>;

  svg: any;
  pack: any;
  transition: number;
  color: any;
  bubbles: Array<any> = [];
  tooltip: any;
  amount = 0;
  type: string;
  hostElement: any;
  hostElementWidth: number;

  constructor(
    private elementRef: ElementRef
  ) {}

  ngOnInit() {
    this.hostElement = this.chartContainer.nativeElement;
  }

  ngOnChanges() {
    if (this.data && this.data.length > 0 && this.svg) this.updateChart();
  }

  ngAfterViewChecked () {
    if(this.data) {
      if (this.hostElement && this.hostElement.offsetWidth !== 0 && this.hostElement.offsetWidth !== this.hostElementWidth) {
        this.hostElementWidth = this.hostElement.offsetWidth;
        d3.select('.bubble-chart svg').remove();
        this.createChart();
        if (this.data.length > 0) this.updateChart();
      }
    }
  }

  createChart = () => {
    this.transition = 700;

    const margin = { top: 0, right: 0, bottom: 0, left: 0};
    const width = this.hostElement.offsetWidth - margin.left - margin.right;
    const height = this.hostElement.offsetHeight - margin.top - margin.bottom;

    this.svg = d3.select(this.hostElement)
      .append('svg')
      .attr('width', '100%')
      .attr('height', '100%');

    this.pack = d3.pack()
      .size([width, height])
      .padding(4);

    this.color = d3.scaleLinear<string>().domain([1, 0, 0, -1])
      .interpolate(d3.interpolateHcl)
      .range(['#1A237E', '#E8EAF6', '#FFEBEE', '#B71C1C']);
    this.tooltip = this.elementRef.nativeElement.querySelector('.tooltip');

    var colorLegend = legend.legendColor()
        .labels(["Very Positive", "Positive", "Neutral", "Negative", "Very Negative"])
        .shapePadding(5)
        .shapeWidth(50)
        .shapeHeight(20)
        .labelOffset(12)
        .title('Sentiment Level')
        .scale(this.color);
    this.svg.append("g")
        .attr("transform", "translate( 0, 84)")
        .call(colorLegend);
  }

  updateChart = () => {
    this.bubbles = this.data;

    const hierarchy = d3.hierarchy({ children: this.bubbles })
      .sum((d: any) => {
        // Crazy stuff.. here in sum we path all the node, not only the leafs
        // So we need to ignore the roots
        if (d.children) return 0;
        return d.weight;
      });

      // JOIN
      const node = this.svg.selectAll('g.data')
        .data(this.pack(hierarchy).leaves(), d => d.data.entity);

      const nodeEnter = node.enter()
        .append('g')
        .attr('class', 'data')
        .attr('transform', d => 'translate(' + d.x + ', ' + d.y + ')');

      // ENTER
      nodeEnter.append('circle')
        .style('fill', '#fff')
        .attr('r', d => d.r)
        .transition()
        .duration(700)
        .style('fill', d => this.color(d.data.sentiment));

      nodeEnter.append('text')
        .attr('fill', d => this.getContrastYIQ(this.color(d.data.sentiment)))
        .attr("text-anchor", "middle")
        .attr("dominant-baseline", "central")
        .attr('pointer-events', 'none')
        .style('font-size', 24 + 'px')
        .style('opacity', 0)
        .text(function(d){return d.data.entity})
        .transition()
        .duration(700)
        .style('opacity', 1)

      // EXIT
      node.select('circle').exit()
        .transition()
        .duration(700)
        .style('opacity', 0)
        .remove();

      node.select('text').exit()
        .transition()
        .duration(700)
        .style('opacity', 0)
        .remove();

      node.exit()
        .transition()
        .duration(700)
        .remove();

      // UPDATE
      node
        .transition()
        .duration(700)
        .attr('transform', d => 'translate(' + d.x + ', ' + d.y + ')')

      node.select('circle').transition()
        .duration(700)
        .attr('r', d => d.r)
        .style('fill', d => this.color(d.data.sentiment));

      node.select('text')
        .text(function(d){return d.data.entity})
        .transition()
        .duration(700)
  }

  getContrastYIQ = (rgbcolor) => {
    rgbcolor = rgbcolor.replace(' ', '');
    var rgbcolors = rgbcolor.split(',');
    rgbcolors[0] = rgbcolors[0].replace('rgb(', '');
    rgbcolors[2] = rgbcolors[2].replace(')', '');

    var r = parseInt(rgbcolors[0],10);
    var g = parseInt(rgbcolors[1],10);
    var b = parseInt(rgbcolors[2],10);
    var yiq = ((r*299)+(g*587)+(b*114))/1000;
    return (yiq < 128) ? 'white' : 'black';
  }

  mouseover = (d, i) => {
    // placement
    this.tooltip.style.visibility = 'visible';
    this.tooltip.style.opacity = 0.9;
    this.tooltip.style.top = d3.event.pageY + 'px';
    this.tooltip.style.left = d3.event.pageX - 300 + 'px';

    // Values
    this.amount = d.data.amount;
    this.type = d.data.type;
  }

  mouseout = () => {
    this.tooltip.style.visibility = 'hidden';
    this.tooltip.style.opacity = 0;
  }
}
