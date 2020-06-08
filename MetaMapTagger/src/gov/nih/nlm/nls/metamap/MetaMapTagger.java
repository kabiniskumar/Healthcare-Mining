package gov.nih.nlm.nls.metamap;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;
import org.apache.commons.csv.CSVRecord;

import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


public class MetaMapTagger {

    public static final String BASE_PATH = "./resources/";
    public static final String INPUT_DIR = "input";

    public static final String skipConceptPath = BASE_PATH + "IgnoredWords.csv";
    private static List<String> skipConcepts = new ArrayList<>();

    public static final String partsOfSpeechPath = BASE_PATH + "IncludePOSTags.csv";
    private static List<String> partsOfSpeech = new ArrayList<>();

    public static long recordNo = 0;
    MetaMapApi api;

    public MetaMapTagger() {
        this.api = new MetaMapApiImpl();
    }


    public MetaMapTagger(String host, int port) {
        this.api = new MetaMapApiImpl();
        this.api.setHost(host);
        this.api.setPort(port);
    }

    public static void main(String[] args) throws Exception {

        File SKIP_CONCEPTS_FILE = new File(skipConceptPath);
        File PARTS_OF_SPEECH_FILE = new File(partsOfSpeechPath);

        setSkipConceptsOrPOSTags(SKIP_CONCEPTS_FILE, skipConcepts);
        setSkipConceptsOrPOSTags(PARTS_OF_SPEECH_FILE, partsOfSpeech);
        initialize();
    }


    private static void setSkipConceptsOrPOSTags(File file, List<String> list) throws IOException {

        Reader reader;
        Iterable<CSVRecord> data;

        reader = new FileReader(file);
        data = getDataUsingReader(reader);

        for (CSVRecord each : data) list.add(each.get(0));
        closeReader(reader);
    }

    private static void closeReader(Reader r) throws IOException {
        if (r != null) r.close();
    }


    private static void initialize() throws Exception {

        int timeout = -1;
        String host;
        int port;

        host = MetaMapApi.DEFAULT_SERVER_HOST;
        port = MetaMapApi.DEFAULT_SERVER_PORT;

        MetaMapTagger mm;
        mm = new MetaMapTagger(host, port);

        List<String> semanticTypes;
        semanticTypes = new ArrayList<>();

        semanticTypes.add("--unique_acros_abbrs_only");
        semanticTypes.add("--composite_phrases");
        semanticTypes.add("4");
        semanticTypes.add("-y");
        semanticTypes.add("--no_derivational_variants");
        semanticTypes.add("--TAGGER_SERVER");
        semanticTypes.add("localhost");
        semanticTypes.add("--restrict_to_sts");
        semanticTypes.add("dsyn,sosy");


        if (timeout > -1) mm.api.setTimeout(timeout);
        mm.api.setOptions(semanticTypes);
        processInputFiles(getCSVFiles(), mm);
    }

    private static File[] getCSVFiles(){
        File dir = new File(INPUT_DIR);
        return dir.listFiles((File directory, String filename) -> filename.endsWith(".csv"));
    }


    private static void processInputFiles(File[] files, MetaMapTagger mm) throws Exception {
        for (File file : files) {
            FileWriter w = new FileWriter(BASE_PATH + file.getName());
            CSVPrinter p = new CSVPrinter(w, CSVFormat.EXCEL.withHeader("PostNumber", "DiseaseId", "DiseaseName", "SymptomId", "SymptomName"));
            processEachFile(file, mm, p, w);
            p.close();
        }
        mm.api.disconnect();
    }


    private static void processEachFile(File file, MetaMapTagger mm, CSVPrinter p, FileWriter w) throws Exception {
        Reader reader = new FileReader(file);

        Iterable<CSVRecord> data = getDataUsingReader(reader);
        recordNo = 0;
        for (CSVRecord each : data) {
            recordNo += 1;
            processEachRecord(each, p, recordNo, mm);
        }
        w.flush();
    }


    private static Iterable<CSVRecord> getDataUsingReader(Reader r) throws IOException {
        return CSVFormat.RFC4180.withFirstRecordAsHeader().parse(r);
    }


    private static void processEachRecord(CSVRecord record, CSVPrinter p, long recordNo, MetaMapTagger mm) throws Exception {
        if (!"".equals(record.get(3)) && !"".equals(record.get(0)))
            mm.runMetaMap(p, recordNo, record.get(3), record.get(0));
    }


    private void runMetaMap(CSVPrinter p, long recordNo, String content, String category) throws Exception {
        List<Result> conditionsFromMetaMap = api.processCitationsFromString(category);
        String[] conditionDetails = new String[2];

        for (Result condition: conditionsFromMetaMap){
            if(condition != null){
                for(Utterance u : condition.getUtteranceList()){
                    for(PCM pcm : u.getPCMList()){
                        for(Mapping map: pcm.getMappingList()){
                            for(Ev mapEv : map.getEvList()){
                                if(mapEv.getSemanticTypes().contains("dsyn")){
                                    conditionDetails[0] = mapEv.getConceptId();
                                    conditionDetails[1] = mapEv.getPreferredName();
                                }
                            }
                        }
                    }
                }
            }
        }
        processResults(content,conditionDetails[0], recordNo, p, conditionDetails[1]);
    }

    private void processResults(String content, String conditionIdFromMetaMap, long recordNo, CSVPrinter p, String conditionNameFromMetaMap) throws Exception {

        List<Result> dataReturnedFromMetaMap = api.processCitationsFromString(content);
        int totalDiseases = 0;
        HashMap<String, String> diseases;
        HashMap<String, String> symptoms;

        diseases = new HashMap<>();
        symptoms = new HashMap<>();

        for (Result data : dataReturnedFromMetaMap){
            if (data != null) {

                for (Utterance utterance : data.getUtteranceList()){
                    for (PCM pcm : utterance.getPCMList()){
                        for (Mapping map : pcm.getMappingList()) {
                            List<Ev> evList = map.getEvList();
                            for (int i = 0, evListSize = evList.size(); i < evListSize; i++) {
                                Ev mapEv = evList.get(i);
                                if (!checkConcepts(mapEv)){

                                    if (!mapEv.getSemanticTypes().contains("dsyn")) {
                                    }
                                    else {
                                        diseases.put(mapEv.getConceptId(), mapEv.getPreferredName());
                                        totalDiseases += 1;
                                    }
                                    if (!mapEv.getSemanticTypes().contains("sosy")) {
                                    }
                                    else {
                                        symptoms.put(mapEv.getConceptId(), mapEv.getPreferredName());
                                    }
                                }
                            }

                        }
                    }
                }

            }
        }

        if (!"".equals(conditionIdFromMetaMap)) {
            if (totalDiseases == 0) {
                diseases.put(conditionIdFromMetaMap, conditionNameFromMetaMap);
            }
        }

        writeRecordsToCSV(diseases, symptoms, recordNo, p);
    }

    private void writeRecordsToCSV(HashMap<String,String> diseases, HashMap<String, String> symptoms, long recordNo, CSVPrinter p) throws IOException {
        if (diseases.size() < 1) {
            this.api.resetOptions();
            return;
        }

        for (Map.Entry<String, String> entry : diseases.entrySet())
            p.printRecord(recordNo, entry.getKey(), entry.getValue(), "", "");
        for (Map.Entry<String, String> entry : symptoms.entrySet())
            p.printRecord(recordNo, "", "", entry.getKey(), entry.getValue());
        this.api.resetOptions();

    }

    private boolean checkConcepts(Ev mapEv) throws Exception {
        Boolean skip = false;

        for (String skipConcept : skipConcepts){
            for (String concept : mapEv.getMatchedWords()){
                if (skipConcept.toLowerCase().equals(concept.toLowerCase())){
                    if (mapEv.getMatchedWords().size()== 1) {
                        skip = true;
                    }
                }
            }
        }
        return skip;
    }

}
