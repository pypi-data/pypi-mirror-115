/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import withStyles, { CSSProperties } from '@material-ui/core/styles/withStyles';
import { TextBox, SubHeader } from '../../core';
import { OutlinedInput, IconButton, Accordion, AccordionSummary, AccordionDetails, withTheme, Theme, CircularProgress, Button, Checkbox } from '@material-ui/core';
import { Global } from '../../Global';
import { FileUploadConfig } from '../../models/FileUploadConfig';
import CloseIcon from '@material-ui/icons/Close'
import CachedIcon from '@material-ui/icons/Cached'
import CheckBoxOutlineBlankIcon from '@material-ui/icons/CheckBoxOutlineBlank';
import CheckBoxIcon from '@material-ui/icons/CheckBox';
import { UploadConfig } from '../../models/UploadConfig';
import FileServerUtils from '../../utils/FileServerUtils';
import { OptumiMetadataTracker } from '../../models/OptumiMetadataTracker';
import { AddFilesPopup } from './AddFilesPopup';
import DirListingItemIcon from './fileBrowser/DirListingItemIcon';
import { FileMetadata } from './fileBrowser/FileBrowser';
import { DataConnectorMetadata } from './dataConnectorBrowser/DataConnectorBrowser';
import { AddDataConnectorsPopup } from './AddDataConnectorsPopup';
import { DataConnectorUploadConfig } from '../../models/DataConnectorUploadConfig';

import { ServerConnection } from '@jupyterlab/services';
import DataConnectorDirListingItemIcon from './dataConnectorBrowser/DataConnectorDirListingItemIcon';
import { ExpandMore, WarningRounded } from '@material-ui/icons';
import { NotificationsPopup } from './NotificationsPopup';
import ExtraInfo from '../../utils/ExtraInfo';
import FormatUtils from '../../utils/FormatUtils';
import { InfoPopup } from '../../core/InfoPoppup';
import WarningPopup from '../../core/WarningPopup';
// import { EmbeddedYoutube } from '../../core/EmbeddedYoutube';

// const emDirNotFile = 'Path is a directory, not a file'
// const emDupPath = 'Duplicate file or directory'
// const emNoPath = 'Unable to find file or directory'

// const bounceAnimation = 'all 333ms cubic-bezier(0.33, 1.33, 0.66, 1) 0s'
const easeAnimation = 'all 150ms ease 0s'

const StyledAccordion = withStyles({
    root: {
        borderWidth: '0px',
        '&.Mui-expanded': {
            margin: '0px',
        },
        '&:before': {
            backgroundColor: 'unset',
        },
    },
})(Accordion)

const StyledAccordionSummary = withStyles({
    root: {
        padding: '0px',
        minHeight: '0px',
        '&.Mui-expanded': {
            minHeight: '0px',
        },
    },
    content: {
        margin: '0px',
        '&.Mui-expanded': {
            margin: '0px',
        },
    },
    expandIcon: {
        padding: '0px',
        marginRight: '0px',
    },
})(AccordionSummary)

const StyledAccordionDetails = withStyles({
    root: {
        display: 'flex',
        flexDirection: 'column',
        padding: '0px',
    },
})(AccordionDetails)

const StyledButton = withStyles({
    root: {
        height: '20px',
        padding: '0px',
        fontSize: '12px',
        lineHeight: '12px',
        minWidth: '0px',
        margin: '0px 6px 6px 6px',
        width: '100%',
    },
    label: {
        height: '20px',
    },
 })(Button);

interface IProps {
    style?: CSSProperties
    openUserDialogTo?: (page: number) => Promise<void> // This is somewhat spaghetti code-y, maybe think about revising
    theme: Theme
}

interface IState {
    filePath: string
    // Here is where we will keep a list of the file paths that were entered successfully but no longer exist on the disk
    localProblemFiles: string[]
    cloudProblemFiles: string[]
    problemDataConnectors: string[]
    filesTooBig: FileMetadata[]
}

class FilesPanel extends React.Component<IProps, IState> {
    private _isMounted = false

    StyledOutlinedInput: any
    textField: React.RefObject<HTMLInputElement>
    timeout: NodeJS.Timeout
    refreshingFiles: boolean
    refreshingDataConnectors: boolean

    constructor(props: IProps) {
        super(props)
        this.StyledOutlinedInput = this.getStyledOutlinedInput()
        this.textField = React.createRef()
        this.state = {
            filePath: '',
            localProblemFiles: [],
            cloudProblemFiles: [],
            problemDataConnectors: [],
            filesTooBig: [],
        }
    }

    private getStyledOutlinedInput = () => {
        return withStyles({
            root: {
                backgroundColor: 'var(--jp-layout-color1)'
            },
            input: {
                fontSize: '12px',
                padding: '3px 6px 3px 6px',
            },
        }) (OutlinedInput);
    }

    private getRequirementsValue = () => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const uploads: UploadConfig = optumi.config.upload;
        return uploads.requirements;
    }

    private saveRequirements = (value: string): string => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const uploads: UploadConfig = optumi.config.upload;
        uploads.requirements = value.replace(' ', '');
        tracker.setMetadata(optumi);
        return '';
    }

    private autoAddPackages = () => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const uploads: UploadConfig = optumi.config.upload;
        const requirements = uploads.requirements;
        const newRequirements = OptumiMetadataTracker.autoAddPackages(requirements, Global.tracker.currentWidget.content.model);
        if (newRequirements != requirements) {
            uploads.requirements = newRequirements;
            tracker.setMetadata(optumi);
        } 
    }

    private pathHasError = (path: string): boolean => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const upload: UploadConfig = optumi.config.upload;
        const files = upload.files;
        for (var i = 0; i < files.length; i++) {
            if (files[i].path === path) return true;
        }
        return false;
    }

    private nameHasError = (name: string): boolean => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const upload: UploadConfig = optumi.config.upload;
        const dataConnectors = upload.dataConnectors;
        for (var i = 0; i < dataConnectors.length; i++) {
            if (dataConnectors[i].name === name) return true;
        }
        return false;
    }

    
    key = 0
    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const optumi = Global.metadata.getMetadata().config;
        const files = optumi.upload.files;
        const dataConnectors = optumi.upload.dataConnectors;
        var yellowTriangle = false
        var redTriangle = false
        for (let file of files) {
            if (file.enabled) {
                if (this.state.localProblemFiles.includes(file.path)) {
                    yellowTriangle = true
                    if (this.state.cloudProblemFiles.includes(file.path)) {
                        redTriangle = true
                    }
                }
            }
        }
        for (let dataConnector of dataConnectors) {
            if (dataConnector.enabled) {
                if (this.state.problemDataConnectors.includes(dataConnector.name)) {
                    redTriangle = true
                }
            }
        }
        return (
            <div style={this.props.style}>
                <StyledAccordion
                    variant={'outlined'}
                    expanded={Global.packagesAccordionExpanded}
                    style={{background: 'var(--jp-layout-color1)'}}
                >
                    <StyledAccordionSummary style={{cursor: 'default'}}>
                        <div style={{display: 'flex'}}>
                            <SubHeader title='Packages'/>
                            <InfoPopup
                                title='Packages'
                                popup={
                                    <div style={{margin: '12px'}}>
                                        <p style={{whiteSpace: 'pre-line'}}>
                                            {`List python packages that your notebook imports. Optumi will pip install these packages onto the machine your session or job will run on.

                                            Each package should go on a separate line:`}
                                        </p>
                                        <img src="https://drive.google.com/uc?export=view&id=1WePvBvaS_6xgvrljKSp8iaijlnD9MFxL" width="350" />
                                        <p style={{whiteSpace: 'pre-line'}}>
                                            {`
                                            To save time you can hit the “Auto-add” button. Optumi will scan your notebook for imported packages and list them for you. However, this is a beta feature and we encourage you to double check that the list is correct.
                                            `}
                                        </p>
                                        {/* <EmbeddedYoutube
                                            name='Demo'
                                            url={'https://www.youtube.com/watch?v=MXzv-XL6LLs'}
                                            width={700}
                                            height={480}
                                        /> */}
                                    </div>
                                }
                            />
                        </div>
                        <span style={{
                            margin: 'auto 15px',
                            flexGrow: 1,
                            textAlign: 'end',
                            opacity: Global.packagesAccordionExpanded ? 0 : 0.5,
                            transitionDuration: '217ms',
                            whiteSpace: 'nowrap',
                            fontSize: '12px',
                            fontStyle: 'italic',
                        }}>
                            {(() => {
                                const requirements = optumi.upload.requirements
                                const numRequirements = requirements === '' ? 0 : requirements.split('\n').filter(line => line !== '').length
                                if (numRequirements > 0) {
                                    return numRequirements + ' requirement' + (numRequirements > 1 ? 's' : '')
                                }
                            })()}
                        </span>
                        <IconButton
                            onClick={() => {
                                Global.packagesAccordionExpanded = !Global.packagesAccordionExpanded
                                if (this._isMounted) this.forceUpdate();
                            }}
                            style={{padding: '0px', marginRight: '-3px', width: '30px', transform: Global.packagesAccordionExpanded ? 'rotate(180deg)' : undefined}}
                        >
                            <ExpandMore />
                        </IconButton>
                    </StyledAccordionSummary>
                    <StyledAccordionDetails>
                        <div style={{width: '100%'}}>
                            <div style={{width: '100%', display: 'inline-flex'}}>
                                <div style={{width: '50%', display: 'inline-flex'}}>
                                    <StyledButton
                                        onClick={this.autoAddPackages}
                                        variant='contained'
                                        disableElevation
                                        color='primary'
                                    >
                                        Auto add
                                    </StyledButton>
                                </div>
                                <div style={{width: '50%', display: 'inline-flex'}} />
                            </div>
                            <TextBox<string>
                                key={optumi.upload.requirements}
                                multiline
                                getValue={this.getRequirementsValue}
                                saveValue={this.saveRequirements}
                                placeholder={'package==version'}
                                style={{padding: '0px 0px 6px 0px'}}
                            />
                        </div>
                    </StyledAccordionDetails>
                </StyledAccordion>
                <StyledAccordion
                    variant={'outlined'}
                    expanded={Global.filesAccordionExpanded}
                    style={{background: 'var(--jp-layout-color1)'}}
                >
                    <StyledAccordionSummary style={{cursor: 'default'}}>
                        <div style={{display: 'flex'}}>
                            <SubHeader title='Files'/>
                            <InfoPopup
                                title='Files'
                                popup={
                                    <div style={{margin: '12px'}}>
                                        <p style={{whiteSpace: 'pre-line'}}>
                                            {`Upload local files and access data from supported databases. Optumi will transfer files to the machine your session or job will run on.`}
                                        </p>
                                        <img src="https://drive.google.com/uc?export=view&id=1scH_eNAfnI5ivkEGfq30fjmpOdBWBmII" width="350" />
                                        {/* <EmbeddedYoutube
                                            name='Demo'
                                            url={'https://www.youtube.com/watch?v=MXzv-XL6LLs'}
                                            width={700}
                                            height={480}
                                        /> */}
                                    </div>
                                }
                            />
                        </div>
                        {(yellowTriangle || redTriangle) && (
                            <ExtraInfo reminder={redTriangle ? 'Files are missing, both locally and in cloud storage. Your notebook will not be able to use them.' : 'Files are missing locally. Your notebook will be able to run with files in cloud storage but we will not be able to sync them with local copies.'}>
                                <WarningRounded fontSize={'small'} style={{color: redTriangle ? this.props.theme.palette.error.main : this.props.theme.palette.warning.main, marginTop: '4px'}} />
                            </ExtraInfo>
                        )}
                        <span style={{
                            margin: 'auto 15px',
                            flexGrow: 1,
                            textAlign: 'end',
                            opacity: Global.filesAccordionExpanded ? 0 : 0.5,
                            transitionDuration: '217ms',
                            whiteSpace: 'nowrap',
                            fontSize: '12px',
                            fontStyle: 'italic',
                        }}>
                            {files.length > 0 && (files.length + ' upload' + (files.length > 1 ? 's' : ''))}{files.length > 0 && dataConnectors.length > 0 ? ', ' : ''}{dataConnectors.length > 0 && (dataConnectors.length + ' connector' + (dataConnectors.length > 1 ? 's' : ''))}
                        </span>
                        <IconButton
                            onClick={() => {
                                Global.filesAccordionExpanded = !Global.filesAccordionExpanded
                                if (this._isMounted) this.forceUpdate();
                            }}
                            style={{padding: '0px', marginRight: '-3px', width: '30px', transform: Global.filesAccordionExpanded ? 'rotate(180deg)' : undefined}}
                        >
                            <ExpandMore />
                        </IconButton>
                    </StyledAccordionSummary>
                    <StyledAccordionDetails>
                        <div style={{display: 'inline-flex', width: '100%'}}>
                            <WarningPopup
                                open={this.state.filesTooBig.length > 0}
                                headerText="Warning"
                                bodyText={(() => {
                                    const problems = this.state.filesTooBig.map(x => x.path + ' (' + FormatUtils.styleCapacityUnitValue()(x.size) + ')').join('\n')
                                    return `The following files exceed the maximum upload size (2 GiB):\n\n` + problems + `\n\nTo access larger data, use data connectors.`
                                })()}
                                continue={{
                                    text: `Ok`,
                                    onContinue: (prevent: boolean) => {
                                        this.safeSetState({ filesTooBig: [] })
                                    },
                                    color: `error`,
                                }}
                            />
                            <AddFilesPopup onFilesAdded={async (metadatas: FileMetadata[]) => {
                                const filesTooBig = [];
                                for (let fileModel of metadatas) {
                                    fileModel.path = Global.convertJupyterPathToOptumiPath(fileModel.path)
                                    // Don't try to add the same file/directory more than once
                                    if (this.pathHasError(fileModel.path)) continue;
                                    const tracker = Global.metadata
                                    const optumi = tracker.getMetadata()
                                    var files = optumi.config.upload.files
                                    if (fileModel.type != 'directory') {
                                        if (fileModel.size > Global.MAX_UPLOAD_SIZE) {
                                            filesTooBig.push(fileModel);
                                        } else {
                                            files.push(new FileUploadConfig({
                                                path: fileModel.path,
                                                type: fileModel.type,
                                                mimetype: fileModel.mimetype,
                                                enabled: true,
                                            }))
                                        }
                                    } else {
                                        const directoryContents = (await FileServerUtils.getRecursiveTree(Global.convertOptumiPathToJupyterPath(fileModel.path)))
                                        const directoryPaths = []
                                        for (let metadata of directoryContents) {
                                            if (metadata.size > Global.MAX_UPLOAD_SIZE) {
                                                filesTooBig.push(metadata);
                                            } else {
                                                directoryPaths.push(metadata.path);
                                            }
                                        }
                                        if (directoryPaths.length > 0) {
                                            files.push(new FileUploadConfig({
                                                path: fileModel.path,
                                                type: fileModel.type,
                                                mimetype: fileModel.mimetype,
                                                enabled: true,
                                            }))
                                        }
                                    }
                                    tracker.setMetadata(optumi)
                                    Global.user.fileTracker.uploadFiles(fileModel)
                                }
                                if (filesTooBig.length > 0) {
                                    this.safeSetState({ filesTooBig: filesTooBig })
                                }
                            }} />
                            <AddDataConnectorsPopup openUserDialogTo={this.props.openUserDialogTo}
								onDataConnectorsAdded={async (metadatas: DataConnectorMetadata[]) => {
                                	for (let dataConnectorModel of metadatas) {
                                    	// Don't try to add the same file/directory more than once
                                    	if (this.nameHasError(dataConnectorModel.name)) continue;
                                    	const tracker = Global.metadata
                                    	const optumi = tracker.getMetadata()
                                    	var dataConnectors = optumi.config.upload.dataConnectors
                                    	dataConnectors.push(new DataConnectorUploadConfig({
                                        	name: dataConnectorModel.name,
                                        	dataService: dataConnectorModel.dataService,
                                    	}))
                                    	tracker.setMetadata(optumi)
                                	}
                            	}
							} />
                        </div>
                        {files.length == 0 && dataConnectors.length == 0 ? (
                            <div
                                style={{
                                fontSize: '12px',
                                lineHeight: '14px',
                                padding: '3px 6px 3px 6px',
                            }}>
                                None
                            </div>
                        ) : (
                            <>
                                {files.map(
                                    (value: FileUploadConfig) => (
                                        <ThemedResourceFile
                                            key={value.path + this.key++}
                                            file={value}
                                            handleFileDelete={() => {
                                                // Cancel the upload
                                                const progress = Global.user.fileTracker.get(value.path);
                                                const compression = progress.filter(x => x.type == 'compression');
                                                const upload = progress.filter(x => x.type == 'upload');
                                                if (compression.length > 0) compression[0].cancel();
                                                if (upload.length > 0) upload[0].cancel();

                                                // Remove the file from metadata
                                                const tracker: OptumiMetadataTracker = Global.metadata;
                                                const optumi = tracker.getMetadata();
                                                const files = optumi.config.upload.files
                                                for (var i = 0; i < files.length; i++) {
                                                    if (files[i].path === value.path) {
                                                        files.splice(i, 1)
                                                        break
                                                    }
                                                }
                                                // optumi.upload.files = (optumi.upload.files as UploadVarMetadata[]).filter(x => x.path !== (event.currentTarget as HTMLButtonElement).id.replace('-delete', ''));
                                                tracker.setMetadata(optumi);
                                                if (this.state.localProblemFiles.includes(value.path)) this.safeSetState({ localProblemFiles: this.state.localProblemFiles.filter(x => x != value.path) });
                                                if (this.state.cloudProblemFiles.includes(value.path)) this.safeSetState({ cloudProblemFiles: this.state.cloudProblemFiles.filter(x => x != value.path) });
                                            }}
                                            handleFileEnabledChange={(enabled: boolean) => {
                                                const tracker: OptumiMetadataTracker = Global.metadata;
                                                const optumi = tracker.getMetadata();
                                                const upload: UploadConfig = optumi.config.upload;
                                                const files = upload.files;
                                                for (var i = 0; i < files.length; i++) {
                                                    const file = files[i];
                                                    if (file.path === value.path) {
                                                        file.enabled = enabled;
                                                        break;
                                                    }
                                                }
                                                tracker.setMetadata(optumi);
                                            }}
                                            missingLocally={this.state.localProblemFiles.includes(value.path)}
                                            missingInCloud={this.state.cloudProblemFiles.includes(value.path)}
                                        />
                                    )
                                )}
                                {dataConnectors.map(
                                    (value: DataConnectorUploadConfig) => (
                                        <ResourceDataConnector
                                            key={value.name + this.key++}
                                            dataConnector={value}
                                            handleFileDelete={() => {
                                                const tracker: OptumiMetadataTracker = Global.metadata;
                                                const optumi = tracker.getMetadata();
                                                const dataConnectors = optumi.config.upload.dataConnectors
                                                for (var i = 0; i < dataConnectors.length; i++) {
                                                    if (dataConnectors[i].name === value.name) {
                                                        dataConnectors.splice(i, 1)
                                                        break
                                                    }
                                                }
                                                // optumi.upload.files = (optumi.upload.files as UploadVarMetadata[]).filter(x => x.path !== (event.currentTarget as HTMLButtonElement).id.replace('-delete', ''));
                                                tracker.setMetadata(optumi);
                                                if (this.state.problemDataConnectors.includes(value.name)) this.safeSetState({ problemDataConnectors: this.state.problemDataConnectors.filter(x => x != value.name) });
                                            }}
                                            noLongerExists={this.state.problemDataConnectors.includes(value.name)}
                                        />
                                    )
                                )}
                            </>
                        )}
                    </StyledAccordionDetails>
                </StyledAccordion>
                <StyledAccordionSummary style={{cursor: 'default'}}>
                    <SubHeader title='Notifications' />
                    <span style={{
                        margin: 'auto 15px',
                        flexGrow: 1,
                        textAlign: 'end',
                        opacity: 0.5,
                        transitionDuration: '217ms',
                        whiteSpace: 'nowrap',
                        fontSize: '12px',
                        fontStyle: 'italic',
                    }}>
                        {(() => {
                            let numEnabled = 0
							const config = Global.metadata.getMetadata().config
                            if (!config.interactive) {
                                const notifications = config.notifications;
                                if (notifications.jobStartedSMSEnabled) numEnabled++;
                                if (notifications.jobFailedSMSEnabled || notifications.jobCompletedSMSEnabled) numEnabled++;
                                // TODO:JJ This currently does not refresh automatically when Global.user.notificationsEnabled changes, and I wasn't sure how to quickly do this.
                                if (Global.user.notificationsEnabled && numEnabled > 0) {
                                    return numEnabled + ' enabled'
                                }
                            }
                        })()}
                    </span>
                    <NotificationsPopup disabled={Global.metadata.getMetadata().config.interactive} openUserDialogTo={this.props.openUserDialogTo} />
                </StyledAccordionSummary>
            </div>
        )
    }

    private refreshFiles = async (poll: boolean = true) => {
        if (this.refreshingFiles) {
            try {
                var newLocalProblemFiles = [];
                var newCloudProblemFiles = [];
                const optumi = Global.metadata.getMetadata().config;
                const files = optumi.upload.files;
                const fileTracker = Global.user.fileTracker;
                for (var file of files) {
                    if (!this.refreshingFiles) break;
                    // Check local
                    const barr = await FileServerUtils.checkIfPathExists(Global.convertOptumiPathToJupyterPath(file.path));
                    if (!barr[0]) {
                        newLocalProblemFiles.push(file.path);
                    } else {
                        // This upload call will 'sync' the file if necessary
                        Global.user.fileTracker.uploadFiles({ path: file.path, type: file.type } as FileMetadata);
                    }
                    // Check cloud
                    const exists = file.type === 'directory' ? fileTracker.directoryExists(file.path) : fileTracker.pathExists(file.path)
                    if (!exists) {
                        newCloudProblemFiles.push(file.path)
                    }
                }
                
                this.safeSetState({ localProblemFiles: newLocalProblemFiles, cloudProblemFiles: newCloudProblemFiles });
            } catch (err) {
                console.error(err)
            }
            if (poll) {
                if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
                setTimeout(this.refreshFiles, 60000);
            }
        }
    }

    private refreshDataConnectors = async (poll: boolean = true) => {
        if (this.refreshingDataConnectors) {
            try {
                const optumi = Global.metadata.getMetadata().config;
                const dataConnectors = optumi.upload.dataConnectors;
                
                const settings = ServerConnection.makeSettings();
                const url = settings.baseUrl + "optumi/get-data-connectors";
                const dataConnectorsFromController: DataConnectorMetadata[] = await (ServerConnection.makeRequest(url, {}, settings).then(response => {
                    if (response.status !== 200) throw new ServerConnection.ResponseError(response);
                    return response.json();
                }).then((json: any) => json.connectors));

                for (var dataConnector of dataConnectors) {
                    if (!this.refreshingDataConnectors) break;
                    if (!this.state.problemDataConnectors.includes(dataConnector.name)) {
                        const exists = dataConnectorsFromController.map(x => x.name).includes(dataConnector.name);
                        if (!exists) {
                            this.safeSetState({ problemDataConnectors: this.state.problemDataConnectors.concat([dataConnector.name]) });
                        }
                    }
                }
            } catch (err) {
                console.error(err)
            }
            if (poll) {
                if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
                setTimeout(this.refreshDataConnectors, 60000);
            }
        }
    }

    private handleDataConnectorChange = () => {
        this.refreshDataConnectors(false)
    }

    private handleMetadataChange = () => {
        this.refreshDataConnectors(false)
        this.refreshFiles(false)
        this.forceUpdate()
    }
	private handleLabShellChange = () => {this.forceUpdate()}

	// Will be called automatically when the component is mounted
	public componentDidMount = () => {
        this._isMounted = true
        this.refreshingFiles = true;
        this.refreshingDataConnectors = true;
        this.refreshFiles();
        this.refreshDataConnectors();
		Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
		Global.labShell.currentChanged.connect(this.handleLabShellChange);
        Global.dataConnectorChange.connect(this.handleDataConnectorChange);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
        Global.labShell.currentChanged.disconnect(this.handleLabShellChange);
        Global.dataConnectorChange.disconnect(this.handleDataConnectorChange);
        this.refreshingFiles = false;
        this.refreshingDataConnectors = false;
        this._isMounted = false
    }

    private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
					}
				}
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
	}
    
    public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
            return false;
        } catch (error) {
            return true;
        }
    }
}
const ThemedFilesPanel = withTheme(FilesPanel)
export { ThemedFilesPanel as FilesPanel }

interface RFProps {
    file: FileUploadConfig,
    handleFileEnabledChange: (enabled: boolean) => void,
    handleFileDelete: () => void,
    missingLocally: boolean,
    missingInCloud: boolean,
    theme: Theme,
}

interface RFState {
    hovering: boolean,
    fileSync: boolean,
}

class ResourceFile extends React.Component<RFProps, RFState> {
    _isMounted: boolean = false

    constructor(props: RFProps) {
        super(props)
        this.state = {
            hovering: false,
            fileSync: this.props.file.enabled,
        }
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const progress = Global.user.fileTracker.get(this.props.file.path);
        const compression = progress.filter(x => x.type == 'compression');
        const upload = progress.filter(x => x.type == 'upload');

        // Decide what color to make this
        // Green is if the file exists on the disk and can be synced
        // Yellow is if it doesn't exist on the disk but exists in the cloud so we can still run
        // Red is if it doesn't exist locally or in the cloud so we can't run
        // Always show is set based on color (green/gray false, red/orange true)
        const palette = this.props.theme.palette;
        var syncColor;
        var alwaysShowFileSync;
        if (this.state.fileSync) {
            if (!this.props.missingLocally) {
                syncColor = palette.success.main;
                alwaysShowFileSync = false;
            } else {
                if (!this.props.missingInCloud) {
                    syncColor = palette.warning.main;
                    alwaysShowFileSync = true;
                } else {
                    syncColor = palette.error.main;
                    alwaysShowFileSync = true;
                }
            }
        } else {
            syncColor = palette.text.disabled;
            alwaysShowFileSync = false;
        }

        return (
            <div
                style={{display: 'flex', width: '100%', position: 'relative'}}
                onMouseOver={() => {
                    this.safeSetState({hovering: true})
                }}
                onMouseOut={() => {
                    this.safeSetState({hovering: false})
                }}
            >
                <div style={{
                    position: 'absolute',
                    left: '-10px',
                    paddingTop: '3px', // The checkbox is 16px, the line is 22px
                    display: 'inline-flex',
                    background: 'var(--jp-layout-color1)',
                    opacity: this.state.hovering ? '1' : '0',
                    transition: easeAnimation,
                }}>
                    <Checkbox
                        disableRipple
                        checked={this.state.fileSync}
                        style={{padding: '0px'}}
                        icon={<CheckBoxOutlineBlankIcon style={{width: '16px', height: '16px'}} />}
                        checkedIcon={<CheckBoxIcon style={{width: '16px', height: '16px'}} />}
                        onClick={() => {
                            let newFileSync = !this.state.fileSync
                            this.safeSetState({fileSync: newFileSync})
                            this.props.handleFileEnabledChange(newFileSync);
                        }}
                    />
                </div>
                <div style={{
                    position: 'absolute',
                    right: '-10px',
                    display: 'inline-flex',
                    background: 'var(--jp-layout-color1)',
                    opacity: this.state.hovering ? '1' : '0',
                    transition: easeAnimation,
                }}>
                    <IconButton onClick={this.props.handleFileDelete} style={{
                        width: '22px',
                        height: '22px',
                        padding: '0px',
                        position: 'relative',
                        display: 'inline-block',
                    }}>
                        <CloseIcon style={{position: 'relative', width: '16px', height: '16px'}} />
                    </IconButton>
                </div>
                <div style={{
                    position: 'absolute',
                    right: '9px',
                    paddingTop: '3px', // The checkbox is 16px, the line is 22px
                    display: 'inline-flex',
                    transition: easeAnimation,
                }}>
                    {(!this.props.missingLocally && (compression.length > 0 || (upload.length > 0 && upload[0].total < 0))) ? (
                        <ExtraInfo reminder={compression.length > 0 ? compression[0].total == -1 ? '' : 'Compressed ' + compression[0].progress + '/' + compression[0].total + ' files' : ''}>
                            <div style={{height: '16px', width: '16px', background: 'var(--jp-layout-color1)'}}>
                                <CircularProgress
                                    color='primary'
                                    size='14px'
                                    thickness={8}
                                    style={{margin: 'auto'}}
                                />
                            </div>
                        </ExtraInfo>
                    ) : (!this.props.missingLocally && (upload.length > 0) ? (
                        <ExtraInfo reminder={FormatUtils.styleCapacityUnitValue()(upload[0].progress) + '/' + FormatUtils.styleCapacityUnitValue()(upload[0].total)}>
                            <div style={{height: '16px', width: '16px', background: 'var(--jp-layout-color1)'}}>
                                <CircularProgress
                                    variant='determinate'
                                    size='14px'
                                    thickness={8}
                                    style={{margin: 'auto'}}
                                    value={(upload[0].progress / upload[0].total) * 100 }
                                />
                            </div>
                        </ExtraInfo>
                    ) : (
                        <CachedIcon style={{
                            position: 'relative',
                            width: '16px',
                            height: '16px',
                            transform: 'scaleX(-1)',
                            color: this.state.fileSync ? syncColor : 'var(--jp-ui-font-color2)',
                            background: 'var(--jp-layout-color1)',
                            opacity: this.state.hovering || alwaysShowFileSync ? this.state.fileSync ? '0.87' : '0.54' : '0',
                        }} />
                    ))}
                </div>
                <div
                    style={{
                        width: '100%',
                        fontSize: '12px',
                        lineHeight: '14px',
                        padding: '3px 6px 3px 6px',
                        display: 'inline-flex',
                    }}
                >
                    <DirListingItemIcon
                        fileType={this.props.file.type}
                        mimetype={this.props.file.mimetype}
                        style={{marginRight: '0px', opacity: this.state.fileSync ? '0.87' : '0.54'}}
                    />
                    <div
                        style={{
                            margin: 'auto 0px',
                            overflow: 'hidden', 
                            color: this.state.fileSync ? 'var(--jp-ui-font-color1)' : 'var(--jp-ui-font-color2)', // this.props.noLongerExists ? '#f48f8d' : ''
                        }}
                        title={
                            (this.props.file.path.includes('/') ? (
`Name: ${this.props.file.path.split('/').pop()}
Path: ${this.props.file.path.replace(/\/[^\/]*$/, '/')}`
                            ) : (
`Name: ${this.props.file.path.split('/').pop()}`
                            ))
                        }
                    >
                        <div style={{
                            direction: 'rtl',
                            overflow: 'hidden', 
                            textOverflow: 'ellipsis', 
                            whiteSpace: 'nowrap',
                        }}>
                            {Global.convertOptumiPathToJupyterPath(this.props.file.path)}
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    private handleFilesChanged = () => this.forceUpdate();

    public componentDidMount = () => {
        this._isMounted = true
        Global.user.fileTracker.getFilesChanged().connect(this.handleFilesChanged)
    }

    public componentWillUnmount = () => {
        Global.user.fileTracker.getFilesChanged().disconnect(this.handleFilesChanged)
        this._isMounted = false
    }

    private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
					}
				}
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
	}

    public shouldComponentUpdate = (nextProps: RFProps, nextState: RFState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
            return false;
        } catch (error) {
            return true;
        }
    }
}

const ThemedResourceFile = withTheme(ResourceFile)

interface RDCProps {
    dataConnector: DataConnectorUploadConfig,
    handleFileDelete: () => void,
    noLongerExists?: boolean,
}

interface RDCState {
    hovering: boolean,
}

class ResourceDataConnector extends React.Component<RDCProps, RDCState> {
    _isMounted: boolean = false

    constructor(props: RDCProps) {
        super(props)
        this.state = {
            hovering: false,
        }
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <div
                style={{display: 'flex', width: '100%', position: 'relative'}}
                onMouseOver={() => {
                    this.safeSetState({hovering: true})
                }}
                onMouseOut={() => {
                    this.safeSetState({hovering: false})
                }}
            >
                <div style={{
                    position: 'absolute',
                    right: '-10px',
                    display: 'inline-flex',
                    background: 'var(--jp-layout-color1)',
                    opacity: this.state.hovering ? '1' : '0',
                    transition: easeAnimation,
                }}>
                    <IconButton onClick={this.props.handleFileDelete} style={{
                        width: '22px',
                        height: '22px',
                        padding: '0px',
                        position: 'relative',
                        display: 'inline-block',
                    }}>
                        <CloseIcon style={{position: 'relative', width: '16px', height: '16px'}} />
                    </IconButton>
                </div>
                <div
                    style={{
                        width: '100%',
                        fontSize: '12px',
                        lineHeight: '14px',
                        padding: '3px 6px 3px 6px',
                        display: 'inline-flex'
                    }}
                >   
                    <DataConnectorDirListingItemIcon
                        dataService={this.props.dataConnector.dataService}
                    />
                    <div
                        style={{
                            margin: 'auto 0px',
                            overflow: 'hidden', 
                            textOverflow: 'ellipsis', 
                            whiteSpace: 'nowrap',
                            direction: 'rtl',
                            color: this.props.noLongerExists ? '#f48f8d' : ''
                        }}
                    >
                        {this.props.dataConnector.name + (this.props.noLongerExists ? ' (no longer exists)' : '')}
                    </div>
                </div>
            </div>
        )
    }

    public componentDidMount = () => {
        this._isMounted = true
    }

    public componentWillUnmount = () => {
        this._isMounted = false
    }

    private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
					}
				}
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
	}

    public shouldComponentUpdate = (nextProps: RDCProps, nextState: RDCState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
            return false;
        } catch (error) {
            return true;
        }
    }
}
