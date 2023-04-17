from lib import generate_srt_file

def get_speaker_list(diarization):
    speaker_list = []
    speaker_mo = ""
    speaker_i = ""
    for track in diarization.itertracks(yield_label=True):
        if track[0].start < 2:
            continue

        # Find the speaker labels
        if not speaker_mo:
            if track[2] == "SPEAKER_00":
                speaker_mo = "SPEAKER_00"
                speaker_i = "SPEAKER_01"
            else:
                speaker_mo = "SPEAKER_01"
                speaker_i = "SPEAKER_00"
        
        if track[2] == speaker_mo:
            speaker_id = "MO"
        elif track[2] == speaker_i:
            speaker_id = "I"
            
        speaker_list.append([track[0].start, track[0].end, speaker_id])
    return speaker_list

def label_transcriptions(transcriptions, speakers):
    """
    Takes a list of transcriptions that includes dictionaries with keys "timestamp" and "text".
    The values of "timestamp" is a list with start time then end time.
    Also takes a list of speakers with start and end times
    and returns a list of transcriptions with start and end times and speaker labels.
    All transcriptions have a speaker label, so label the transcriptions with the closest
    matching speaker label. This means labeling by finding the closest matching start time in combination with end time.
    If a transcription has a start time that is before the first speaker label, then
    label the transcription with the first speaker label.

    Args:
    - transcriptions: a list of dictionaries with keys "timestamp" and "text"
    - speakers: a list of dictionaries with keys "start_time", "end_time", and "speaker_label"

    Returns:
    - labeled_transcriptions: a list of dictionaries with keys "start_time", "end_time", "speaker_label", and "text"
    """

    # labeled_transcriptions = []

    # # Find the first speaker label
    # if speakers[0][0] > transcriptions[0]["timestamp"][0]:
    #     speaker_index = 0
    # else:
    #     speaker_index = 1

    # for transcription in transcriptions:
    #     # Find the closest matching speaker label
    #     closest_speaker_index = speaker_index
    #     if abs(transcription["timestamp"][0] - speakers[speaker_index][1]) < abs(transcription["timestamp"][0] - speakers[speaker_index][0]):
    #         closest_speaker_index = speaker_index + 1
    #         closest_start_diff = abs(transcription["timestamp"][0] - speakers[speaker_index+1][0])
    #         closest_end_diff = abs(transcription["timestamp"][1] - speakers[speaker_index+1][1])
    #     else:
    #         closest_speaker_index = speaker_index
    #         closest_start_diff = abs(transcription["timestamp"][0] - speakers[speaker_index][0])
    #         closest_end_diff = abs(transcription["timestamp"][1] - speakers[speaker_index][1])

    #     for i, speaker in enumerate(speakers):
    #         start_diff = abs(transcription["timestamp"][0] - speaker[0])
    #         end_diff = abs(transcription["timestamp"][1] - speaker[1])

    #         if start_diff + end_diff < closest_start_diff + closest_end_diff:
    #             if abs(transcription["timestamp"][0] - speaker[1]) < start_diff:
    #                 continue

    #             closest_speaker_index = i
    #             closest_start_diff = start_diff
    #             closest_end_diff = end_diff

        # Add the transcription to the labeled_transcriptions list

    labeled_transcriptions = []

    for transcription in transcriptions:
        # If the median of transcription is inside of timerange of speaker, then label it with that speaker
        transcription_median = (transcription["timestamp"][0] + transcription["timestamp"][1]) / 2
        closest_speaker_index = find_bucket(speakers, transcription_median)
        if closest_speaker_index == 0:
            # Do the same but round down the median to closest integer
            transcription_median = int(transcription_median)
            closest_speaker_index = find_bucket(speakers, transcription_median)


        labeled_transcriptions.append({
            "timestamp": [transcription["timestamp"][0],transcription["timestamp"][1]],
            "text": speakers[closest_speaker_index][2] + ": " + transcription["text"],
            "speaker_label": speakers[closest_speaker_index][2]
        })

    return labeled_transcriptions

def find_bucket(speakers, transcription_median):
    closest_speaker_index = 0
    for i, speaker in enumerate(speakers):
        if transcription_median >= speaker[0] and transcription_median <= speaker[1]:
            closest_speaker_index = i
            break
    return closest_speaker_index





example_speaker_list = [[5.104687500000001, 7.2309375, 'MO'], [8.361562500000002, 21.2709375, 'I'], [21.4734375, 24.3253125, 'MO'], 
 [22.2496875, 22.6209375, 'I'], [23.3971875, 23.7515625, 'I'], [25.0846875, 33.0834375, 'I'], 
 [33.33656250000001, 34.70343750000001, 'MO'], [34.1465625, 34.855312500000004, 'I'], [35.462812500000005, 40.0359375, 'I'], 
 [37.268437500000005, 37.63968750000001, 'MO'], [40.626562500000006, 42.7696875, 'I'], 
 [42.19593750000001, 44.423437500000006, 'MO'], [45.23343750000001, 57.3328125, 'I'], 
 [56.42156250000001, 58.682812500000004, 'MO'], [59.1215625, 63.88031250000001, 'I'], 
 [63.8634375, 67.8290625, 'MO'], [64.5215625, 66.4621875, 'I'], [67.4746875, 69.5334375, 'I'], 
 [69.8034375, 71.0015625, 'MO'], [70.6978125, 77.1778125, 'I'], [77.7853125, 80.0634375, 'I'], 
 [79.9790625, 82.1053125, 'MO'], [80.9915625, 81.2784375, 'I'], [83.3709375, 105.3928125, 'I'], 
 [95.4871875, 96.3478125, 'MO'], [102.0515625, 110.5734375, 'MO'], [106.1353125, 109.6115625, 'I'], 
 [111.1303125, 114.1003125, 'I'], [114.4378125, 115.4334375, 'MO'], [114.8090625, 118.3359375, 'I'], 
 [118.3359375, 120.1415625, 'MO'], [119.28093750000001, 123.8371875, 'I'], [124.0565625, 126.3684375, 'MO'], 
 [125.37281250000001, 125.6765625, 'I'], [127.5496875, 138.4509375, 'I'], [133.5234375, 135.51468749999998, 'MO'], 
 [138.2653125, 139.24406249999998, 'MO'], [139.80093750000003, 147.2765625, 'I'], [143.2940625, 149.18343750000003, 'MO'], 
 [149.95968750000003, 153.23343749999998, 'MO'], [149.9765625, 152.17031250000002, 'I'], [154.1615625, 158.1609375, 'I'], 
 [156.7940625, 159.24093750000003, 'MO'], [160.70906250000002, 167.64468750000003, 'I'], 
 [167.50968749999998, 171.1040625, 'MO'], [169.0284375, 169.3828125, 'I'], [172.8253125, 178.7653125, 'I'], 
 [177.80343750000003, 179.8959375, 'MO'], [181.3978125, 190.2740625, 'I'], [181.98843750000003, 182.93343750000003, 'MO'], 
 [190.81406250000003, 193.48031250000003, 'MO'], [191.3203125, 191.92781250000002, 'I'], [195.4040625, 200.2134375, 'I'], 
 [199.1671875, 200.9896875, 'MO'], [201.17531250000002, 202.17093750000004, 'I'], [203.3859375, 208.2965625, 'I'], 
 [206.3390625, 206.87906250000003, 'MO'], [207.8409375, 212.1609375, 'MO'], [210.77718750000003, 215.6878125, 'I'], 
 [216.4134375, 219.82218749999998, 'I'], [220.3959375, 225.6271875, 'MO'], [220.51406250000002, 220.9528125, 'I'], 
 [223.46718750000002, 223.85531250000003, 'I'], [226.60593749999998, 230.2340625, 'I'], 
 [228.68156249999998, 228.8334375, 'MO'], [230.04843750000003, 233.9971875, 'MO'], 
 [231.8878125, 232.5290625, 'I'], [234.6046875, 235.7184375, 'I'], [236.02218750000003, 237.4059375, 'MO'], 
 [238.0471875, 240.2578125, 'I'], [241.01718750000003, 243.1434375, 'MO'], [245.1178125, 248.8303125, 'MO'], 
 [249.6740625, 254.51718750000003, 'I'], [253.99406249999998, 256.42406250000005, 'MO'], 
 [257.0990625, 264.37218750000005, 'I'], [257.7065625, 258.56718750000005, 'MO'], 
 [264.67593750000003, 266.09343750000005, 'MO'], [267.6796875, 271.45968750000003, 'MO'], 
 [271.12218750000005, 275.1721875, 'I'], [272.5059375, 272.6409375, 'MO'], [275.30718750000005, 277.68656250000004, 'MO'], 
 [276.4715625, 276.8259375, 'I'], [278.3109375, 283.0528125, 'I'], [283.3396875, 288.06468750000005, 'MO'], 
 [284.50406250000003, 284.92593750000003, 'I'], [287.5584375, 292.4690625, 'I'], [291.4903125, 293.9540625, 'MO'], 
 [294.1903125, 297.1096875, 'I'], [297.2953125, 303.11718750000006, 'MO'], [301.3621875, 301.7503125, 'I'], 
 [303.84281250000004, 308.44968750000004, 'I'], [308.97281250000003, 315.1490625, 'MO'], 
 [311.30156250000005, 311.79093750000004, 'I'], [315.09843750000005, 316.6678125, 'I'], 
[315.90843750000005, 316.11093750000003, 'MO'], [317.59593750000005, 321.46031250000004, 'I']
]

example_predictions = [{'timestamp': (0.0, 2.0), 'text': ' Telefon ringer.'}, {'timestamp': (5.0, 8.0), 'text': ' Ner. Nødvendig ambulansen, er pasienten våken?'}, {'timestamp': (8.0, 12.0), 'text': ' Ja, ja, ja. Eller, ja, jeg tror det.'}, {'timestamp': (12.0, 17.0), 'text': ' Det er Arne og Rasmus som ringer, og jeg ringer om kona mi, Margit.'}, {'timestamp': (17.0, 20.0), 'text': ' Hun er 87 år og ligger på bakken og kommer ikke opp nå.'}, {'timestamp': (20.0, 22.0), 'text': ' Jeg vet ikke helt hva jeg skal gjøre.'}, {'timestamp': (22.0, 25.04), 'text': ' Nei, men jeg skal hjelpe deg. Hvilken adress er dere på?'}, {'timestamp': (28.0, 29.0), 'text': ' Vi er i øvre Frydendal, 437.'}, {'timestamp': (33.04, 33.32), 'text': ' Ute på Frydendal, ute i Askeles.'}, {'timestamp': (34.84, 35.4), 'text': ' Ja, er dere ute?'}, {'timestamp': (37.12, 37.16), 'text': ' Nei, vi er inne i leiligheten vår.'}, {'timestamp': (37.56, 40.0), 'text': ' Ja. I sjøttetetasje leiligheten vår.'}, {'timestamp': (40.56, 42.08), 'text': ' Vi står to rødstakke på ringkrokka.'}, {'timestamp': (42.12, 42.64), 'text': ' Ja.'}, {'timestamp': (43.12, 44.44), 'text': ' Hva er det som skjedde for noe?'}, {'timestamp': (45.0, 48.0), 'text': ' Nei, jeg hadde bare vært på toalett, og når jeg kom ut igjen så ligger hun på bakken her.'}, {'timestamp': (48.0, 51.0), 'text': ' Margit, er du våken? Margit? Ja da, hun ser på meg altså.'}, {'timestamp': (51.0, 54.0), 'text': ' Ja. Hun ligger på bakken, og jeg får hun ikke opp der altså.'}, {'timestamp': (54.0, 57.0), 'text': ' Hun husker ikke selv, så jeg kler ikke å løfte opp Margit, hun er en store dame.'}, {'timestamp': (57.0, 59.0), 'text': ' Ja, svar hun ordentlig når du snakker med henne?'}, {'timestamp': (59.0, 62.0), 'text': ' Margit, ja, Margit. Ja da, hun svarer. Hun sier hun har vondt da, hun har slått seg litt.'}, {'timestamp': (62.0, 66.4), 'text': ' Hun har vondt i hofta, sier hun. Vondt i hofta, ja. Vondt i hofta, ja, ja, ja, stakkar.'}, {'timestamp': (66.4, 67.4), 'text': ' Ja, for hun puster normalt.'}, {'timestamp': (67.4, 69.4), 'text': ' Nei, ursa meg, dette her var ikke bra. Hva sa du?'}, {'timestamp': (69.4, 71.4), 'text': ' For hun puster normalt.'}, {'timestamp': (71.4, 77.4), 'text': ' Ja, ja. Ja da, hun, det ser ut som hun puster ganske vanlig. Ja, Margit, får du puste? Ja.'}, {'timestamp': (77.4, 79.9), 'text': ' Ja da, Margit puster. Ja, det går greit med pusten, sier hun.'}, {'timestamp': (79.9, 82.4), 'text': ' Ja, husker hun hvorfor hun falt?'}, {'timestamp': (82.4, 84.4), 'text': ' Vet du hvorfor du falt, Margit?'}, {'timestamp': (84.4, 85.0), 'text': ' Ja. Nei, nei, hun vet ikke hva som Vet du hvorfor hun falt, Margit?'}, {'timestamp': (85.0, 85.5), 'text': ' Nei.'}, {'timestamp': (85.5, 92.0), 'text': ' Nei, hun vet ikke hva som skjedde. Hun sier hun plutselig så hun skulle bare reise opp og gå og hente noe, hun lå jo på gulvet. Hun er litt sur etter altså.'}, {'timestamp': (92.0, 95.0), 'text': ' Så det er ikke alltid jeg får gode svar, men hun sier at hun ikke vet hva som skjedde.'}, {'timestamp': (95.0, 96.0), 'text': ' Okei, Tor.'}, {'timestamp': (96.0, 99.0), 'text': ' Kanskje hun har snublet i noe, jeg vet ikke. Det er noen tepper her, vi har de tepper.'}, {'timestamp': (100.0, 102.0), 'text': ' Kanskje, jeg vet ikke.'}, {'timestamp': (102.0, 103.0), 'text': ' Nei, nei.'}, {'timestamp': (103.0, 105.0), 'text': ' Jeg tror nesten vi trenger en ambulanse og litt hjelp altså.'}, {'timestamp': (105.0, 108.0), 'text': ' Ja, vi skal hjelpe dere. Vi skal sende en ambulanse og hjelpe dere.'}, {'timestamp': (108.0, 109.0), 'text': ' Ja, tusen takk.'}, {'timestamp': (109.0, 111.0), 'text': ' Men det er Hofda som sier hun har vondt i.'}, {'timestamp': (111.0, 114.0), 'text': ' Hun har vondt i Hofda, ja. Og så sier hun at hun er litt svibbel.'}, {'timestamp': (114.0, 115.0), 'text': ' Hun er svibbel, ja.'}, {'timestamp': (115.0, 118.0), 'text': ' Kører ikke helt og snurrer litt, sier hun. Rommet snurrer litt.'}, {'timestamp': (118.0, 120.0), 'text': ' Ja, kanskje hun falt fordi hun var svimmel.'}, {'timestamp': (120.0, 124.0), 'text': ' For deg Erik, er det det da? Ja, kanskje, jeg vet ikke. Jeg tror ikke jeg får noe svar på det altså.'}, {'timestamp': (124.0, 126.0), 'text': ' Nei. Pleier hun Nico å være svimmel?'}, {'timestamp': (126.0, 134.0), 'text': ' Nei hun har ikke vært svimmel, nei det hun har ikke pleiet å pleie på det. Litt når hun reiser seg opp da. Sånn som ja alltid der alle viser meg da, men ikke noe mer enn det. Nei da.'}, {'timestamp': (134.0, 135.0), 'text': ' Nei, har hun ikke vært så blitt svimmel i dag da?'}, {'timestamp': (135.0, 138.0), 'text': ' Hun pleier ikke det. Ja kanskje hun har blitt, ja jeg tror nesten det altså.'}, {'timestamp': (138.0, 139.0), 'text': ' Er hun svimmel nå?'}, {'timestamp': (139.0, 146.2), 'text': ' Hun har en time hos fastlegen nå etterpå, egentlig klokka 11 altså. Så nå kommer Pimas sykehvilje uansett og kikker på denne kassa.'}, {'timestamp': (146.2, 146.7), 'text': ' Ja.'}, {'timestamp': (146.7, 149.4), 'text': ' Så kan vi ta det der med fastlegene etter det.'}, {'timestamp': (149.4, 150.4), 'text': ' Ja.'}, {'timestamp': (150.4, 150.9), 'text': ' Ja.'}, {'timestamp': (150.9, 151.9), 'text': ' Ja, det er faktisk bra det.'}, {'timestamp': (151.9, 153.4), 'text': ' Men er det der Margit Svimmel nå?'}, {'timestamp': (153.4, 156.7), 'text': ' Ja, hun sier at hun er i Svimmel der hun ligger. Ja.'}, {'timestamp': (156.7, 159.4), 'text': ' Ja, er det sånn at hun selv holder på å besvime?'}, {'timestamp': (159.4, 164.4), 'text': ' Holder hun på å besvime Margit? Ja, hun sier det.'}, {'timestamp': (164.4, 164.9), 'text': ' Ja.'}, {'timestamp': (164.9, 167.6), 'text': ' Hun føler seg litt sånn på å snu litt og holde på å besvime litt ja.'}, {'timestamp': (167.6, 171.0), 'text': ' Ja akkurat. Klarer hun å snakke normalt synes du?'}, {'timestamp': (171.0, 178.0), 'text': ' Margit hører du meg? Ja da hun svarer meg med vanlig. Ja hun gjør det. Klarer hun å snakke altså.'}, {'timestamp': (178.0, 182.0), 'text': ' Kan du si heller å smile til deg? Ja. Klarer hun det?'}, {'timestamp': (182.0, 186.0), 'text': ' Margit kan du smile?? Ja, ja da. Jeg husker ikke pent.'}, {'timestamp': (186.0, 191.0), 'text': ' Nei, alltid smiler pent, Margit. Jeg husker ikke pent nå også. Ja. Det går bra.'}, {'timestamp': (191.0, 194.0), 'text': ' Og greier hun å løpe armene sine når hun ligger der?'}, {'timestamp': (194.0, 199.0), 'text': ' Jeg vet ikke. Hun ligger nå liksom på den høyre armen der da, så det er ikke så lett å se.'}, {'timestamp': (199.0, 201.0), 'text': ' Nei, det er ikke så lett å få undersøkt.'}, {'timestamp': (201.0, 206.0), 'text': ' Nei, nei. Nei, jeg vet ikke. Det var jo ikke sånn denne dagen skulle være. Nei. Hun ligger der. Nei, nei. Nei, jeg vet ikke. Det var ikke sånn denne dagen skulle være.'}, {'timestamp': (206.0, 207.0), 'text': ' Nei.'}, {'timestamp': (207.0, 208.0), 'text': ' Hun ligger ikke der. Nei, nei.'}, {'timestamp': (208.0, 212.0), 'text': ' Kan du spørre henne om hun følte seg ustød da hun gikk i sted?'}, {'timestamp': (212.0, 217.0), 'text': ' Ja. Margit, hvor følte du deg ustød, husker du, Margit? Nei, hun vet ikke.'}, {'timestamp': (217.0, 218.0), 'text': ' Nei, hun vet ikke det.'}, {'timestamp': (218.0, 220.0), 'text': ' Hun bare kikker på meg og rister på hodet. Nei, hun klarer det ikke.'}, {'timestamp': (220.0, 226.0), 'text': ' Men i Øvre Fryndal 437 er det leilighet eller et hus?'}, {'timestamp': (226.0, 228.0), 'text': ' Nei, der er blokk 16 etasjer.'}, {'timestamp': (228.0, 229.0), 'text': ' Der er blokk ja.'}, {'timestamp': (229.0, 230.0), 'text': ' Så vi bor i 16 etasje.'}, {'timestamp': (230.0, 231.0), 'text': ' Dere bor i 16 etasje ja.'}, {'timestamp': (231.0, 232.0), 'text': ' Ja, ja.'}, {'timestamp': (232.0, 234.0), 'text': ' Hva er det som står på ringklokka dere så?'}, {'timestamp': (234.0, 236.0), 'text': ' Der står det Toralsdottir.'}, {'timestamp': (236.0, 237.0), 'text': ' Toraldottir?'}, {'timestamp': (237.0, 240.0), 'text': ' Ja, det stemmer. Ja, med H.'}, {'timestamp': (240.0, 243.0), 'text': ' Åja. Sånn.'}, {'timestamp': (245.0, 249.0), 'text': ' Okei, men da er det en ambulans på vei for å se på kona din nå.'}, {'timestamp': (249.0, 254.0), 'text': ' Ja, det er bra. Vil du slå opp noe på Margit eller trenger du fødselsnummeren hennes?'}, {'timestamp': (254.0, 256.0), 'text': ' Ja, har du fødselsnummeren hennes da?'}, {'timestamp': (256.0, 266.5), 'text': ' Ja da. 2709, ja, 27097745312. Det kan jeg. 27 ja ja.'}, {'timestamp': (268.5, 270.5), 'text': ' Ja, men takk det var vet du.'}, {'timestamp': (270.5, 272.5), 'text': ' Har det gitt noe bra med det?'}, {'timestamp': (272.5, 275.5), 'text': ' Ja, så bra. Nei men da venter vi bare her da, så kommer en ambulanse.'}, {'timestamp': (275.5, 276.5), 'text': ' Ja, men da ligger hun.'}, {'timestamp': (276.5, 277.0), 'text': ' Ja.'}, {'timestamp': (277.0, 278.5), 'text': ' Skal hun ligge eller?'}, {'timestamp': (278.5, 280.5), 'text': ' Ja, hun har det ikke så veldig bra sånn som hun ligger.'}, {'timestamp': (280.5, 282.5), 'text': ' Jeg tror ikke jeg tørrer å flytte på henne.'}, {'timestamp': (282.5, 283.5), 'text': ' Hun er en stor dame vet du.'}, {'timestamp': (283.5, 284.5), 'text': ' Ja, ja.'}, {'timestamp': (284.5, 287.0), 'text': ' Også hvis hun har skadet hofta så er stor dame, vet du. Ja, ja. Også hvis hun har skadet hofta si også oppi dette.'}, {'timestamp': (287.0, 289.0), 'text': ' Ja, ja. Det er kanskje best å forsøke det da.'}, {'timestamp': (289.0, 291.0), 'text': ' Jeg tror hun legger meg med det. Har du lang tid da før bilen kommer?'}, {'timestamp': (291.0, 294.0), 'text': ' Nei, hun har ikke noen lang tid. Jeg er rett rundt hjørnet det allerede.'}, {'timestamp': (294.0, 297.0), 'text': ' Ja, ja, men det er supert. Ja, men tusen takk da.'}, {'timestamp': (297.0, 303.0), 'text': ' Ja, hvis det til hun blir noe verre eller det skjer noe endring nå før ambulansen er der, så skal du bare ringe tilbake igjen til meg da.'}, {'timestamp': (303.0, 305.0), 'text': ' Da skal jeg ringe tilbake igjen.'}, {'timestamp': (305.0, 308.0), 'text': ' Ja, det er greit. Og den time hos fastlegen må vi kanskje bare abestille.'}, {'timestamp': (309.0, 311.0), 'text': ' Ja, det kan nok tenkes det.'}, {'timestamp': (311.0, 314.0), 'text': ' Men hvis du er litt i tvil, så kan du vente til sykebilen har kommet, ja.'}, {'timestamp': (314.0, 315.0), 'text': ' Da skal de hjelpe deg.'}, {'timestamp': (315.0, 316.0), 'text': ' Ja, det kan vi gjøre.'}, {'timestamp': (316.0, 317.0), 'text': ' Ja.'}, {'timestamp': (317.0, 318.0), 'text': ' Ja.'}, {'timestamp': (318.0, 319.0), 'text': ' Okei. Tusen takk da.'}, {'timestamp': (319.0, 320.0), 'text': ' Ja, ha det da.'}, {'timestamp': (320.0, 321.0), 'text': ' Ha det, ha det.'}]

labeled_predictions = label_transcriptions(example_predictions, example_speaker_list)

print("speaker_list:")
print(example_speaker_list)
print("----------------")
print("labeled_predictions:")
print(labeled_predictions)

generate_srt_file(labeled_predictions, "output_lydlogg-2.srt")
