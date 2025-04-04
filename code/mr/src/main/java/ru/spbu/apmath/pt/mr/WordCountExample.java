package ru.spbu.apmath.pt.mr;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.log4j.Logger;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.ru.RussianAnalyzer;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import ru.spbu.apmath.pt.util.LoggerUtils;

import java.io.IOException;


public class WordCountExample extends Configured implements Tool {
    private static final Logger LOG = Logger.getLogger(WordCountExample.class);

    public static void main(final String[] args) throws Exception {
        LoggerUtils.initLogger();
        ToolRunner.run(new Configuration(), new WordCountExample(), args);
    }

    @Override
    public int run(final String[] args) throws Exception {
        final Job job = Job.getInstance(getConf());
        job.setJobName("wordcount");
        job.setJarByClass(WordCountExample.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        job.setCombinerClass(TextReducer.class);

        // указываем Mapper и Reducer
        job.setMapperClass(TextMapper.class);
        job.setReducerClass(TextReducer.class);

        // удаляем директорию куда будет писаться результат
        FileSystem.get(getConf()).delete(new Path(args[1]), true);
        job.setInputFormatClass(TextInputFormat.class);
        job.setOutputFormatClass(TextOutputFormat.class);

        FileInputFormat.setInputPaths(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        job.waitForCompletion(true);

        return 0;
    }

    public static class TextMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
        private static final IntWritable ONE = new IntWritable(1);

        private final Text textBuffer = new Text();

        // компонент из Lucene, простой токенайзер.
        private final Analyzer сlassicAnalyzer = new RussianAnalyzer();

        @Override
        protected void map(final LongWritable key, final Text value, final Context context)  {
            try {
                final TokenStream ts = сlassicAnalyzer.tokenStream("", value.toString());
                ts.reset();

                // проходим по всем "словам"
                while(ts.incrementToken()) {
                    final CharSequence word = ts.getAttribute(CharTermAttribute.class);
                    final String str = word.toString();

                    textBuffer.set(str);
                    context.write(textBuffer, new IntWritable(1));
                }
                ts.close();
            } catch (Exception ex) {
                LOG.error("", ex);
            }

        }
    }

    public static class TextReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        @Override
        protected void reduce(final Text key, final Iterable<IntWritable> values, final Context context) throws IOException, InterruptedException {
            int s = 0;
            for (IntWritable v : values) {
                s += v.get();
            }

            if (s > 2) {
                context.write(key, new IntWritable(s));
            }
        }
    }
}