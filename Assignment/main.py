import os
import sys
from vmtranslator import VMReader, AssemblyBuilder
def processSingleFile(vmFile, emitter):
    emitter.setFile(vmFile)
    reader = VMReader(vmFile)

    while reader.hasNext():
        reader.advance()
        cmdType = reader.type()

        if cmdType == VMReader.ARITH:
            emitter.writeMath(reader.arg1())

        elif cmdType in (VMReader.PUSH, VMReader.POP):
            emitter.writePushPop(cmdType, reader.arg1(), reader.arg2())

        elif cmdType == VMReader.LABEL:
            emitter.label(reader.arg1())

        elif cmdType == VMReader.GOTO:
            emitter.goTo(reader.arg1())

        elif cmdType == VMReader.IF:
            emitter.ifGo(reader.arg1())

        elif cmdType == VMReader.FUNCTION:
            emitter.defineFunc(reader.arg1(), reader.arg2())

        elif cmdType == VMReader.CALL:
            emitter.callFunc(reader.arg1(), reader.arg2())

        elif cmdType == VMReader.RETURN:
            emitter.doReturn()


def collectVMFiles(path):
    if os.path.isfile(path):
        return [path], False

    vmList = [
        os.path.join(path, f)
        for f in os.listdir(path)
        if f.endswith(".vm")
    ]

    vmList.sort()
    return vmList, True


def getOutputPath(sourcePath):
    if os.path.isfile(sourcePath):
        return sourcePath.replace(".vm", ".asm")
    return os.path.join(sourcePath, os.path.basename(sourcePath) + ".asm")


def runTranslator(inputPath):
    vmFiles, needsBootstrap = collectVMFiles(inputPath)
    outputFile = getOutputPath(inputPath)

    builder = AssemblyBuilder(outputFile)

    if needsBootstrap:
        builder.bootstrap()

    for file in vmFiles:
        processSingleFile(file, builder)

    builder.save()
    print(f"Output saved to {outputFile}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <file.vm | directory>")
        sys.exit(1)

    srcPath = sys.argv[1].rstrip(" ")
    runTranslator(srcPath)