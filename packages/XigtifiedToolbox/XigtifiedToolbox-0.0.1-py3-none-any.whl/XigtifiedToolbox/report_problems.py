from mom.XigtifiedToolbox.util import fetch_igts

class ProblemReport:
    def report_inconsistencies(self, toolbox_file, reftag, lang_line_tag, tags, problems, xc):
        with open(toolbox_file, 'r') as f:
            toolbox_lines = f.readlines()
        nonemtpy_toolbox_lines = [l for l in toolbox_lines if l.strip()]
        toolbox_igts = self.parse_toolbox(nonemtpy_toolbox_lines, reftag, tags)
        output_lines = []
        for igt_id in problems:
            tb_id = igt_id
            if len(problems[igt_id]) > 0:
                toolbox_entry = toolbox_igts.get(igt_id)
                if not toolbox_entry:
                    tb_id = igt_id[3:]
                    toolbox_entry = toolbox_igts.get(tb_id) #maybe 'igt' was prepended by xigt
                    if not toolbox_entry:
                        fetch_igts(xc,[igt_id])
                        raise Exception('Toolbox entry with reference {0} not found'.format(igt_id))
                text = toolbox_entry[lang_line_tag]
                w_ids = []
                comments = []
                for p in problems[igt_id]:
                    w_id,word = p.split('\t')
                    w_ids.append(w_id)
                    comment = problems[igt_id][p]
                    comments.append(comment + ' in word #{0} ({1})\n'.format(w_id,word))
                    additional_comment = self.create_additional_comment(comment,toolbox_entry,w_id)
                    comments.append(additional_comment)
                self.construct_output_entry(toolbox_entry,w_ids,output_lines,toolbox_lines,reftag,tb_id,comments)
        with open('problems.txt', 'w') as f:
            for ln in output_lines:
                if ln:
                    f.write(ln)

    def create_additional_comment(self,comment,toolbox_entry,w_id):
        if comment.startswith('No gloss'):
            return "COMMENT: Probably a missing or extra space somewhere in the IGT.\n"

    def construct_output_entry(self,toolbox_entry,word_ids,output_lines,toolbox_lines,reftag,igt_id,comments):
        relevant_lines = self.find_toolbox_lines(toolbox_lines,reftag,igt_id)
        output_lines.append("****PROBLEMATIC ENTRY ID: {0}****\n".format(igt_id))
        output_lines.append("PROBLEM CODE(s) AS DETECTED BY XIGT:\n")
        output_lines.extend(comments)
        output_lines.append('\n')
        output_lines.extend(relevant_lines)
        output_lines.append('\n')

    # def detect_misalignment(self,toolbox_igt):
    #     misalignments = []
    #     first_line = toolbox_igt[0]
    #     for i,c in enumerate(first_line):
    #         for ln in toolbox_igt[1:]:
    #             if not (c == ' ' and ln[i] == ' ') or not (c != ' ' and ln[i] != ' '):
    #                 misalignments.append(i)
    #     return misalignments




    def parse_toolbox(self, toolbox_lines, reftag, tags):
        igts = {}
        i = 0
        while i < len(toolbox_lines)-1:
            while not toolbox_lines[i].startswith(reftag) and i < len(toolbox_lines)-1:
                i += 1
            cur_id = toolbox_lines[i].strip()[5:] # strip the newline and the \\ref tag.
            igts[cur_id] = {}
            i += 1
            prev_tag = None
            while i < len(toolbox_lines) - 1 and not toolbox_lines[i].startswith(reftag):
                tag = toolbox_lines[i].split(' ')[0]
                if not tag.startswith('\\'):
                    if not prev_tag:
                        raise Exception('Why was prev_tag not been initialized?')
                    if prev_tag in tags:
                        igts[cur_id][prev_tag].append(toolbox_lines[i])
                else:
                    prev_tag = tag
                    if tag in tags:
                        if not tag in igts[cur_id]:
                            igts[cur_id][tag] = []
                        igts[cur_id][tag].append(toolbox_lines[i])
                i += 1
        return igts

    def find_toolbox_lines(self, toolbox_lines, reftag, igt_id):
        relevant_lines = []
        i=0
        while i < len(toolbox_lines) - 1 and not toolbox_lines[i].startswith(reftag + ' ' + igt_id):
            i += 1
        while i < len(toolbox_lines) - 1 and not toolbox_lines[i+1].startswith(reftag):
            relevant_lines.append(toolbox_lines[i])
            i += 1
        return relevant_lines
