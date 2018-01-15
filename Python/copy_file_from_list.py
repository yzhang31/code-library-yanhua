import os
import shutil

file_list = ["\\\\analytics.dir.slb.com\\repository\\Bbc7Cdb4-B776-4B01-B8B8-F87Fed507852\\ComputationService.19-Jan-2017.00-19-20.2868MiniDump.dmp",
"\\\\analytics.dir.slb.com\\repository\\Ffa77De1-5312-49B9-86C1-493Bd5D371D8\\ExeJobManager.03-May-2017.11-42-39.4044MiniDump.dmp",
"\\\\analytics.dir.slb.com\\repository\\Ffa77De1-5312-49B9-86C1-493Bd5D371D8\\ExeJobManager.03-May-2017.11-53-37.4832MiniDump.dmp",
"\\\\analytics.dir.slb.com\\repository\\Ffa77De1-5312-49B9-86C1-493Bd5D371D8\\ExeJobManager.03-May-2017.13-50-09.6824MiniDump.dmp",
"\\\\analytics.dir.slb.com\\repository\\E1D1E01B-0E24-41Cc-A212-96F4E3F51A5D\\ExeJobManager.30-Mar-2017.09-33-59.3680MiniDump.dmp",
"\\\\analytics.dir.slb.com\\repository\\Ee11D2C4-0Ce2-4857-Aafb-8Efdfb4186E0\\ExeJobManager.14-Mar-2017.14-45-31.10160MiniDump.dmp",
"\\\\analytics.dir.slb.com\\repository\\87Dd3787-5421-4E55-Bbc7-2Eb15C79D2E8\\ExeJobManager.31-Jan-2017.18-09-15.5716MiniDump.dmp",
"\\\\analytics.dir.slb.com\\repository\\851Bc2D9-A63F-4C2D-Bd5E-B46C49Abe1F3\\ComputationService.03-Feb-2017.10-16-02.7728MiniDump.dmp",
"\\\\analytics.dir.slb.com\\repository\\87Dd3787-5421-4E55-Bbc7-2Eb15C79D2E8\\ExeJobManager.31-Jan-2017.18-03-35.3568MiniDump.dmp",
"\\\\analytics.dir.slb.com\\repository\\752A174A-955D-44Ab-93D4-88Fa65Acdc9C\\ExeJobManager.31-Jan-2017.21-21-15.6428MiniDump.dmp",
"\\\\analytics.dir.slb.com\\repository\\87Dd3787-5421-4E55-Bbc7-2Eb15C79D2E8\\ExeJobManager.31-Jan-2017.18-06-54.3188MiniDump.dmp",
"\\\\analytics.dir.slb.com\\repository\\90Ce6E2B-4958-4990-8F27-893Fdfdf9Ca6\\ComputationService.16-Feb-2017.03-38-38.6488MiniDump.dmp",
"\\\\analytics.dir.slb.com\\repository\\87Dd3787-5421-4E55-Bbc7-2Eb15C79D2E8\\ExeJobManager.31-Jan-2017.17-58-12.536MiniDump.dmp",
"\\\\analytics.dir.slb.com\\repository\\36A60C9B-7Fa6-4E34-Bb29-5E2303Ebfc0A\\ExeJobManager.31-Jan-2017.18-35-36.5700MiniDump.dmp",
"\\\\analytics.dir.slb.com\\repository\\8D7Dfef3-1B25-477D-931C-4B72366444A9\\ExeJobManager.13-Feb-2017.20-47-58.816MiniDump.dmp",
"\\\\analytics.dir.slb.com\\repository\\9Bad2774-9D75-4115-9Ad9-1Bc98541D80F\\ExeJobManager.21-Jun-2017.08-57-41.8936MiniDump.dmp",
"\\\\analytics.dir.slb.com\\repository\\8D7Dfef3-1B25-477D-931C-4B72366444A9\\ExeJobManager.13-Feb-2017.20-36-20.4400MiniDump.dmp"]

for file in file_list:
    shutil.copy2(file, "d:\\temp")
