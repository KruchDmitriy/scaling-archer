function [] = train_annot2txt(matInp, path)
data = load(matInp);

disp('--------------------------------------------------------------');
disp('Converting Stanford train annotation to text file.');
disp('Number of training samples:');
kData = length(data.annotations);
disp(kData);
f = fopen(path, 'w');
fprintf(f, 'image\t\tx1\ty1\tx2\ty2\tclass\n');
for i = 1:kData
    sample = data.annotations(i);
    fprintf(f, strcat(sample.fname, '\t'));
    fprintf(f, strcat(int2str(sample.bbox_x1), '\t'));
    fprintf(f, strcat(int2str(sample.bbox_y1), '\t'));
    fprintf(f, strcat(int2str(sample.bbox_x2), '\t'));
    fprintf(f, strcat(int2str(sample.bbox_y2), '\t'));
    fprintf(f, strcat(int2str(sample.class), '\n'));
end
fclose(f);
disp('--------------------------------------------------------------');
