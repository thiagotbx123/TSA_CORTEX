/**
 * Linear Ticket Poster
 * Creates worklog tickets in Linear
 */

import { LinearClient, Team, IssueLabel } from '@linear/sdk';
import {
  LinearPostRequest,
  LinearPostResult,
  WorklogOutput,
  Config,
  RoleRouting,
} from '../types';
import { getLinearCredentials } from '../utils/config';
import { formatDisplay } from '../utils/datetime';
import { renderLinearBody } from '../worklog/markdown';
import { renderNarrativeWorklog } from '../worklog/narrative';
import { SpineHubData } from '../spinehub';

export interface NarrativeOptions {
  generationTimeMs: number;
  version: string;
  spineHub?: SpineHubData;
}

export class LinearPoster {
  private client: LinearClient | null = null;
  private config: Config;

  constructor(config: Config) {
    this.config = config;
  }

  async initialize(): Promise<boolean> {
    const creds = getLinearCredentials();
    if (!creds.apiKey) {
      return false;
    }
    this.client = new LinearClient({ apiKey: creds.apiKey });
    return true;
  }

  async postWorklog(
    worklog: WorklogOutput,
    role: string = 'default',
    dryRun: boolean = false,
    narrativeOpts?: NarrativeOptions
  ): Promise<LinearPostResult> {
    if (!this.client) {
      const initialized = await this.initialize();
      if (!initialized) {
        return {
          success: false,
          error_message: 'Linear API key not configured',
          created_at: new Date().toISOString(),
        };
      }
    }

    try {
      // Get routing config
      const routing = this.config.role_routing[role] || this.config.role_routing['default'];
      if (!routing) {
        return {
          success: false,
          error_message: `No routing config found for role: ${role}`,
          created_at: new Date().toISOString(),
        };
      }

      // Find team
      const team = await this.findTeam(routing.linear_team);
      if (!team) {
        return {
          success: false,
          error_message: `Team not found: ${routing.linear_team}`,
          created_at: new Date().toISOString(),
        };
      }

      // Generate title - [Worklog]YY_MM_DD TSA Name format
      const endDateObj = new Date(worklog.run_metadata.end_datetime);
      const yy = endDateObj.getFullYear().toString().slice(2);
      const mm = (endDateObj.getMonth() + 1).toString().padStart(2, '0');
      const dd = endDateObj.getDate().toString().padStart(2, '0');
      const title = `[Worklog]${yy}_${mm}_${dd} TSA ${worklog.run_metadata.person_display_name}`;

      // Generate body - use narrative format if options provided
      let body: string;
      if (narrativeOpts) {
        body = renderNarrativeWorklog(worklog, {
          ownerName: worklog.run_metadata.person_display_name,
          startDate: new Date(worklog.run_metadata.start_datetime),
          endDate: endDateObj,
          generatedAt: new Date(),
          generationTimeMs: narrativeOpts.generationTimeMs,
          version: narrativeOpts.version,
          spineHub: narrativeOpts.spineHub,
        });
      } else {
        body = renderLinearBody(worklog);
      }

      // Find labels
      const labelIds = await this.findLabels(team.id, routing.labels);

      if (dryRun) {
        console.log('\n=== DRY RUN - Would create ticket: ===');
        console.log(`Team: ${routing.linear_team}`);
        console.log(`Title: ${title}`);
        console.log(`Labels: ${routing.labels.join(', ')}`);
        console.log('\nBody preview:');
        console.log(body.slice(0, 500) + '...');
        console.log('\n=== END DRY RUN ===\n');

        return {
          success: true,
          issue_id: 'DRY_RUN',
          issue_url: 'https://linear.app/dry-run',
          created_at: new Date().toISOString(),
        };
      }

      // Create issue
      const issue = await this.client!.createIssue({
        teamId: team.id,
        title,
        description: body,
        labelIds: labelIds.length > 0 ? labelIds : undefined,
        projectId: routing.project,
        assigneeId: routing.assignee,
      });

      const createdIssue = await issue.issue;

      return {
        success: true,
        issue_id: createdIssue?.identifier,
        issue_url: createdIssue?.url,
        created_at: new Date().toISOString(),
      };
    } catch (error: any) {
      return {
        success: false,
        error_message: error.message,
        created_at: new Date().toISOString(),
      };
    }
  }

  private async findTeam(teamName: string): Promise<Team | null> {
    try {
      const teams = await this.client!.teams();
      for (const team of teams.nodes) {
        if (
          team.name.toLowerCase() === teamName.toLowerCase() ||
          team.key.toLowerCase() === teamName.toLowerCase()
        ) {
          return team;
        }
      }
      return null;
    } catch {
      return null;
    }
  }

  private async findLabels(teamId: string, labelNames: string[]): Promise<string[]> {
    const ids: string[] = [];

    try {
      const team = await this.client!.team(teamId);
      const labels = await team.labels();

      for (const labelName of labelNames) {
        for (const label of labels.nodes) {
          if (label.name.toLowerCase() === labelName.toLowerCase()) {
            ids.push(label.id);
            break;
          }
        }
      }
    } catch {
      // Ignore label errors
    }

    return ids;
  }

  async getTeams(): Promise<Array<{ id: string; name: string; key: string }>> {
    if (!this.client) {
      await this.initialize();
    }

    if (!this.client) {
      return [];
    }

    try {
      const teams = await this.client.teams();
      return teams.nodes.map((t) => ({
        id: t.id,
        name: t.name,
        key: t.key,
      }));
    } catch {
      return [];
    }
  }
}

export async function postToLinear(
  worklog: WorklogOutput,
  config: Config,
  role: string = 'default',
  dryRun: boolean = false,
  narrativeOpts?: NarrativeOptions
): Promise<LinearPostResult> {
  const poster = new LinearPoster(config);
  return poster.postWorklog(worklog, role, dryRun, narrativeOpts);
}
