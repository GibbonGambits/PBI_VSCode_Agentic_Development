# Tooling, workflow and AI assistance

Part 1 of 3 of this topic. Covers: Scripting with TOM and APIs; Choosing development tools; Translations and renaming objects.

Practice notes drawn from public SQLBI articles and white papers, each restated in new words. They are information, not rules to enforce: the checklist and this template's standards win. Each note gives its ID, then its strength (Must, Should, Consider, Option or Fact), the year of the article and the article's address, when it applies, and any version limit. **Check** after the strength means the note may no longer hold in current Power BI: confirm it with the skill `pbi-lookup` before you rely on it. The article holds the detail. A note may name a tool, a website or a custom visual that this template does not use, or describe publishing, deploying or changing a deployed model: that is information for the developer. You do not install, call or suggest such a tool, and nothing is published or deployed from this template.

## General practice

### Scripting with TOM and APIs

**T16-A014-2.** Custom .NET code that queries an Analysis Services database should use the ADOMD.NET client library, not an OLE DB connection, for DAX, MDX and DMX alike: its command object accepts parameters and still returns results through a DataReader.
- Should. Check. 2012. https://www.sqlbi.com/articles/execute-dax-queries-through-ole-db-and-adomd-net/
- When: Your own .NET code sends DAX, MDX or DMX queries to an Analysis Services Tabular database.
- Version: In 2012 ADOMD.NET was a separate download in the SQL Server Feature Pack.

### Choosing development tools

**T16-A049-1.** A developer can pick a separate tool per job: DAX Studio to write and run DAX queries, DAX Formatter to lay out code, Tabular Editor to edit a model definition offline, VertiPaq Analyzer for memory use and compression, BISM Normalizer to compare and merge models.
- Option. Check. 2014. https://www.sqlbi.com/articles/tools-for-dax-and-tabular-developers/
- When: Picking tools for writing DAX and developing Tabular, Power Pivot or Power BI models.
- Version: 2014 list; it also names SSAS Tabular Translator, DAX Patterns, DAX Editor, BIDS Helper and Excel Power Pivot add-ins.

**T16-A221-1.** Decide at the very start of a project whether the Tabular model is built in Power BI Desktop or in Visual Studio: a project cannot move from one of these two to the other later. Tabular Editor can be brought in at any point.
- Should. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: Starting a Tabular model project with Microsoft tools.
- Version: Describes the tools as of 2021.

**T16-A221-9.** Keep ALM Toolkit among the model development tools: it compares two models, Analysis Services databases or Power BI datasets, shows their differences, and merges them or generates a file that deploys them.
- Should. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: Comparing and merging two versions of one semantic model, a small part of the development cycle.
- Version: A tool outside this template: information for the developer, never called or suggested by Copilot.

**T16-A221-12.** For enterprise-level Tabular models, developers should take Tabular Editor as their main development tool, free or commercial edition by productivity needs and budget: it alone reaches every model feature in every situation, also for a model first made in Power BI Desktop.
- Should. Check. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: Enterprise-level models on Power BI Premium or Analysis Services.
- Version: 2021 view: the free, open-source edition is Tabular Editor 2; Tabular Editor 3 is the commercial one. A tool outside this template: information for the developer, never called or suggested by Copilot.

**T16-A221-13.** Developers should keep DAX Studio in their toolset and use it to write and tune DAX queries, measures and data models, checking query results, query plans and performance.
- Should. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: Developing and optimising Tabular models and their DAX code.
- Version: A tool outside this template: information for the developer, never called or suggested by Copilot.

**T16-A221-18.** Do not expect one all-in-one tool. For each need, select the tools that reach the required model features most productively: no single monolithic tool serves model authors, report authors and business users alike.
- Should. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: Assembling the toolset for model authors, report authors and business users.

**T16-A221-19.** Starting a Tabular project in Visual Studio (Analysis Services Projects) can open more features shared with Analysis Services, such as custom partitions. In return, Power BI-specific features such as Incremental Refresh are out of reach, and Power BI Desktop cannot edit the deployed model.
- Option. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: Choosing the authoring tool at the start of a Tabular project for Analysis Services or Power BI Premium.
- Version: Describes the tools as of 2021.

**T16-A331-3.** No tool is mandatory; pick one for a specific model task: design sketches (Figma, Excalidraw), Tabular Editor, Bravo, Analyze in Excel, DAX Studio, VertiPaq Analyzer, ALM Toolkit, Measure Killer, DAX Optimizer, pbi-tools, Fabric notebooks, DAX query view, TMDL view, Performance Analyzer, VS Code.
- Option. 2025. https://www.sqlbi.com/articles/tools-in-power-bi/
- When: Choosing a tool for model design, DAX debugging, optimisation, comparison, usage analysis, source control, testing or bulk changes.
- Version: Tabular Editor 2 is free with basic features, version 3 is paid; Fabric notebooks need a Fabric capacity.

**T16-A331-4.** Possible tools for report tasks: design tools for mock-ups and wireframes, Power Designer (a Fabric workload) for themes, generative AI for custom visuals (DAX SVG, R, Python, Deneb), Deneb templates, PBI Explorer to compare versions, PBI Inspector for best-practice rules, Fabric notebooks for bulk changes.
- Option. 2025. https://www.sqlbi.com/articles/tools-in-power-bi/
- When: Choosing a tool for report design, theming, custom visuals, version comparison, rule checks or bulk formatting.
- Version: PBI Inspector V2 and notebook report functions need PBIR; notebooks need Fabric capacity. R and Python visuals retire May 2027.

### Translations and renaming objects

**T16-A050-2.** Weigh a rename against clients outside the project too: an Excel PivotTable connected to the model drops the measures and columns renamed since its last refresh.
- Consider. Check. 2014. https://www.sqlbi.com/articles/frictionless-renaming-in-tabular-models-with-analysis-services/
- When: Renaming a table, column or measure of a model that Excel workbooks already use.
- Version: Written in 2014 for Power Pivot and Analysis Services Tabular, which then offered no rename refactoring.

## Special-case techniques and facts

### Scripting with TOM and APIs

**T16-A014-1.** A .NET program that sends a DAX query through the OLE DB classes with the MSOLAP provider fails with an error as soon as a command parameter is attached to the query. The only known way around it is ADOMD.NET.
- Fact. Check. 2012. https://www.sqlbi.com/articles/execute-dax-queries-through-ole-db-and-adomd-net/
- When: Custom .NET code running parameterised DAX queries on Analysis Services over an OLE DB connection.
- Version: Reported in 2012 as an unfixed defect of the .NET OLE DB assembly; check whether it still applies.

**T16-A084-1.** To change a Tabular model at compatibility level 1200 from code, prefer the Tabular Object Model (TOM) classes: at that level the object model maps one to one onto the physical entities of the database, and TOM exposes them.
- Should. 2016. https://www.sqlbi.com/articles/adding-a-measure-to-a-tabular-model/
- When: Programmatic edits of a deployed model, such as measures created by an add-in or generated variants.
- Version: Compatibility level 1200 arrived with Analysis Services 2016; TOM ships as a namespace of the AMO library. This template changes a model only in its files, never through a server or a library.

**T16-A084-2.** For a model at the older 110x compatibility level, the Tabular AMO 2012 library is one way to get an object model similar to TOM; at that level one model table is split into several server objects, which makes direct access harder.
- Option. Check. 2016. https://www.sqlbi.com/articles/adding-a-measure-to-a-tabular-model/
- When: Programmatic access to Tabular models at the 110x compatibility level.
- Version: 110x belongs to Analysis Services 2012 and 2014; the library was published on CodePlex. This template changes a model only in its files, never through a server or a library.

**T16-A084-3.** A C# project that edits a Tabular model through TOM needs references to two assemblies: Microsoft.AnalysisServices.Tabular, which holds the TOM classes, and Microsoft.AnalysisServices.Core, which is needed to connect to Analysis Services.
- Must. 2016. https://www.sqlbi.com/articles/adding-a-measure-to-a-tabular-model/
- When: Writing C# code that connects to Analysis Services to add or change model objects.
- Version: This template changes a model only in its files, never through a server or a library.

**T16-A084-4.** To add a measure to a deployed model through TOM: connect to the server, navigate to the database, its model and the target table, then add a new Measure object to that table's Measures collection.
- Must. 2016. https://www.sqlbi.com/articles/adding-a-measure-to-a-tabular-model/
- When: Adding a measure to a deployed Analysis Services model from C# or PowerShell.
- Version: This template changes a model only in its files, never through a server or a library.

**T16-A084-5.** Although a measure name is unique in the whole model, each measure belongs to one table, and that home table influences Q&A semantics in Power BI and drillthrough behaviour in Excel.
- Fact. 2016. https://www.sqlbi.com/articles/adding-a-measure-to-a-tabular-model/
- When: Judging what the home table of a measure changes for client tools.
- Version: Stated in 2016. This template keeps every measure in one measures table (model standard rule 1). This template changes a model only in its files, never through a server or a library.

**T16-A084-6.** To change through TOM a measure that may already exist, look it up with the Find method of the table's Measures collection; create and add a new Measure object only when the lookup returns nothing.
- Must. 2016. https://www.sqlbi.com/articles/adding-a-measure-to-a-tabular-model/
- When: Replacing a measure's expression, or creating the measure when missing, in a deployed model from C# or PowerShell.
- Version: This template changes a model only in its files, never through a server or a library.

**T16-A084-7.** After adding or changing objects through TOM, call SaveChanges on the model object. Until then the edits exist only in the client-side copy; the call sends all pending edits to the server in one transaction.
- Must. 2016. https://www.sqlbi.com/articles/adding-a-measure-to-a-tabular-model/
- When: Any measure created or modified through TOM in C# or PowerShell.
- Version: This template changes a model only in its files, never through a server or a library.

**T16-A084-8.** A PowerShell script that edits a Tabular model must first load the Microsoft.AnalysisServices.Tabular assembly to reach the TOM classes; after that it follows the same steps as the C# code.
- Must. 2016. https://www.sqlbi.com/articles/adding-a-measure-to-a-tabular-model/
- When: Adding or replacing measures in a deployed model from PowerShell.
- Version: This template changes a model only in its files, never through a server or a library.

**T16-A084-9.** To add or replace one measure in a deployed model, prefer TOM to TMSL: the TMSL CreateOrReplace command cannot target a single measure, so the definitions of all tables would have to be deployed.
- Should. Check. 2016. https://www.sqlbi.com/articles/adding-a-measure-to-a-tabular-model/
- When: Adding or replacing a single measure in a deployed model.
- Version: State of TMSL in 2016; a later release may have added this support. This template changes a model only in its files, never through a server or a library.

**T16-A205-2.** Token-acquisition code is not enough. The application must also be registered and configured in Azure Active Directory, API permissions included, so that the service principal the code relies on exists and is authorised.
- Must. Check. 2020. https://www.sqlbi.com/articles/creating-a-service-principal-account-for-power-bi-api/
- When: An application uses a service principal to obtain an access token for the Power BI API.
- Version: Written in 2020 under the name Azure Active Directory.

**T16-A205-3.** The Power BI API does not authenticate callers itself. A service principal gets its access token from Azure Active Directory services, reached through separate libraries such as the Microsoft Authentication Library (MSAL).
- Fact. Check. 2020. https://www.sqlbi.com/articles/creating-a-service-principal-account-for-power-bi-api/
- When: Building an application that calls the Power BI API under a service principal identity.
- Version: Written in 2020 under the name Azure Active Directory.

**T16-A221-17.** Scripts in .NET Core languages, PowerShell included, can build Tabular models and deploy them through the XMLA endpoint to Analysis Services or Power BI Premium, also from operating systems other than Windows.
- Option. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: Automating the creation or deployment of Tabular models.
- Version: Microsoft released the TOM and ADOMD.NET libraries for .NET Core in February 2021. Nothing is published or deployed from this template: this is a person's or a pipeline's step.

### Choosing development tools

**T16-A221-2.** A Tabular model built in Visual Studio cannot be opened in Power BI Desktop, whether deployed to Power BI Premium from Visual Studio or restored there from an Analysis Services backup. Desktop-only features such as Incremental Refresh stay out of reach with Microsoft tools.
- Fact. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: Moving an Analysis Services model, or one developed in Visual Studio, to Power BI Premium.
- Version: Stated in 2021; restoring an Analysis Services backup into Premium was announced from April 2021.

**T16-A221-3.** Before configuring Incremental Refresh with Tabular Editor on a model published to Power BI Premium, make sure its compatibility level is at least 1450. Raising the level requires deploying the model from Tabular Editor as a new database.
- Must. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: A Premium model that Power BI Desktop cannot edit needs Incremental Refresh, set up through Tabular Editor.
- Version: Stated in 2021.

**T16-A221-4.** A Power BI Desktop model published to Premium can be neither edited in nor imported into Visual Studio. Tabular Editor can extract it, but database properties and data sources need manual fixes before publishing to Azure Analysis Services; on-premises servers may need more.
- Fact. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: Moving a model from Power BI Premium to Analysis Services.
- Version: Stated in 2021: Analysis Services did not support the enhanced metadata format Power BI uses.

**T16-A221-5.** Partitions beyond those of Incremental Refresh can be managed after publishing with SQL Server Management Studio or a PowerShell script built on the TOM libraries. Tabular Editor can also manipulate partitions on any Tabular model, whatever the server or compatibility level.
- Option. Check. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: A model authored in Power BI Desktop and published to Power BI Premium needs custom partitions.
- Version: Stated in 2021.

**T16-A221-6.** Once any tool changes a model published from Power BI Desktop through the XMLA endpoint, Power BI Desktop can no longer edit the published model. It can then only edit the original local file or a PBIX downloaded from the service.
- Fact. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: A model authored in Power BI Desktop and published to Power BI Premium.
- Version: Stated in 2021; external tools can deploy and edit Premium models through XMLA endpoints since January 2021.

**T16-A221-11.** Visual Studio's relationship editor gives a many-to-many cardinality relationship a Both filter direction and offers no way to change it. Power BI Desktop can change it; for a Visual Studio model, hand-edit model.bim or use another editor such as Tabular Editor.
- Fact. Check. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: A model edited with Visual Studio needs a relationship of many-to-many cardinality.
- Version: Reported in 2021; many-to-many cardinality relationships exist since Analysis Services 2019.

**T16-A221-14.** Changing a model with Tabular Editor or ALM Toolkit does not forfeit Microsoft support: Microsoft supports any valid model deployed to its specification, such as a valid model.bim deployed through the TOM library. The third-party tools themselves are not built or supported by Microsoft.
- Fact. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: An organisation hesitates to use third-party tools on Tabular models for fear of losing Microsoft support.

**T16-A221-15.** In Visual Studio, prefer the integrated workspace to a separate Analysis Services workspace instance. Visual Studio keeps the workspace in step with every edit, so the workspace should sit close to the editor to keep latency low.
- Should. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: Developing a Tabular model in Visual Studio.

**T16-A221-16.** For a large model, Tabular Editor can edit the model.bim file disconnected from any workspace, or synchronise with a connected workspace only on demand. That avoids the wait after every edit that Power BI Desktop and Visual Studio impose.
- Option. 2021. https://www.sqlbi.com/articles/development-tools-for-tabular-models-in-2021/
- When: Models holding hundreds of tables and measures, where per-edit synchronisation passes one second.
- Version: True of Tabular Editor 2 and Tabular Editor 3 in 2021.

**T16-A331-6.** To get outside advice on a model without handing over sensitive data, one option is to extract a .vpax file, or an obfuscated .ovpax file, with VertiPaq Analyzer and share that file.
- Option. 2025. https://www.sqlbi.com/articles/tools-in-power-bi/
- When: Asking someone outside the team to review a model that holds sensitive data.

### Translations and renaming objects

**T16-A050-3.** Translations can serve as a renaming layer: build the model in a language no user works in, or add a translation for the model's own locale, and set the user-facing names there. Clients show the translated names; DAX and MDX queries keep the originals.
- Option. Check. 2014. https://www.sqlbi.com/articles/frictionless-renaming-in-tabular-models-with-analysis-services/
- When: User-facing names must change without editing DAX; possibly unsupported by Microsoft, so test first and accept the risk.
- Version: 2014 technique for Analysis Services Tabular through BIDS Helper; not available in Power Pivot. Microsoft's guidance in this template uses default-language translations sparingly (multiple languages, rule 3).

**T16-A081-2.** Upgrading a Tabular model to compatibility level 1200 discards every metadata translation that was added with BIDS Helper. Those translations must then be rebuilt from scratch or carried over with a separate migration procedure.
- Fact. 2016. https://www.sqlbi.com/articles/translations-in-analysis-services-2016/
- When: Migrating a compatibility level 110x Tabular model that holds BIDS Helper translations to level 1200.
- Version: Level 110x translations used an unsupported Multidimensional technique that only MDX clients such as Excel displayed.

**T16-A081-3.** Save a Tabular translation file as Unicode UTF-8, the encoding the export writes and the import expects. In Visual Studio set it explicitly with Save with Encoding (Advanced Save Options): a JSON file with no character above code 127 is otherwise saved as ANSI.
- Must. Check. 2016. https://www.sqlbi.com/articles/translations-in-analysis-services-2016/
- When: Editing JSON translation files of an Analysis Services Tabular model.
- Version: Visual Studio behaviour as described in 2016.

**T16-A081-4.** An Excel PivotTable whose connection string forces a specific culture shows translated metadata and so can check Tabular translations; Analyze in Excel in Visual Studio lets you choose that culture.
- Must. Check. 2016. https://www.sqlbi.com/articles/translations-in-analysis-services-2016/
- When: Testing metadata translations of an Analysis Services Tabular model.
- Version: In July 2016 Excel was the only Microsoft client showing Tabular translations; Power BI live connections did not.

**T16-A081-5.** Translate hidden objects as well. The translation file lists every object whatever its visibility, although hidden objects are never displayed to users, so this is not strictly needed.
- Should. 2016. https://www.sqlbi.com/articles/translations-in-analysis-services-2016/
- When: Translating the metadata of an Analysis Services Tabular model.

**T16-A081-6.** Export each language to a translation file of its own. Several languages in one file can become complex to handle, above all without a dedicated editor.
- Should. 2016. https://www.sqlbi.com/articles/translations-in-analysis-services-2016/
- When: Exporting translation files from an Analysis Services Tabular model.

**T16-A081-7.** Do not rename model objects once a translation file has been exported: importing a translation that names a since-renamed object fails. If a rename happened anyway, repeat it inside the translation file or restore the original name before the import.
- Should. 2016. https://www.sqlbi.com/articles/translations-in-analysis-services-2016/
- When: A translation file has been exported from an Analysis Services Tabular model.

**T16-A081-8.** Leave the translation of model metadata to the very end of the project. Objects created after an export are not translated by the import, a new export always holds every object, and partial translations cannot be merged.
- Should. 2016. https://www.sqlbi.com/articles/translations-in-analysis-services-2016/
- When: Projects that translate Analysis Services Tabular metadata through exported translation files.

**T16-A081-9.** Consider a dedicated editor such as SSAS Tabular Translator for translation files: it shows each object's original and translated names on one row, which speeds the work, and handles several languages in one file.
- Consider. Check. 2016. https://www.sqlbi.com/articles/translations-in-analysis-services-2016/
- When: Editing Tabular translation files, whose JSON any text editor opens but which is not user-friendly.

**T16-A081-10.** A translation file is plain text, so no particular tool is needed: it can be edited in any text editor that handles UTF-8, or through a script of your own that turns the JSON into a simpler format.
- Option. 2016. https://www.sqlbi.com/articles/translations-in-analysis-services-2016/
- When: Editing JSON translation files exported from an Analysis Services Tabular model, outside Visual Studio.
