using System;
using System.Collections.Generic;
using System.Data.Common;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using Newtonsoft.Json;
using Npgsql;
using StackExchange.Redis;

namespace Worker
{
    public class Program
    {
        public static int Main(string[] args)
        {
            try
            {
                var pgsql = OpenDbConnection("Server=db;Username=postgres;");
                var redisConn = OpenRedisConnection("redis");
                var redis = redisConn.GetDatabase();

                // Keep alive is not implemented in Npgsql yet. This workaround was recommended:
                // https://github.com/npgsql/npgsql/issues/1214#issuecomment-235828359
                var keepAliveCommand = pgsql.CreateCommand();
                keepAliveCommand.CommandText = "SELECT 1";

                var definition = new { vote = "", voter_id = "" };
                while (true)
                {
                    // Slow down to prevent CPU spike, only query each 100ms
                    Thread.Sleep(100);

                    // Reconnect redis if down
                    if (redisConn == null || !redisConn.IsConnected) {
                        Console.WriteLine("Reconnecting Redis");
                        redisConn = OpenRedisConnection("redis");
                        redis = redisConn.GetDatabase();
                    }
                    string json = redis.ListLeftPopAsync("votes").Result;
                    if (json != null)
                    {
                        var vote = JsonConvert.DeserializeAnonymousType(json, definition);
                        Console.WriteLine($"Processing vote for '{vote.vote}' by '{vote.voter_id}'");
                        // Reconnect DB if down
                        if (!pgsql.State.Equals(System.Data.ConnectionState.Open))
                        {
                            Console.WriteLine("Reconnecting DB");
                            pgsql = OpenDbConnection("Server=db;Username=postgres;");
                        }
                        else
                        { // Normal +1 vote requested
                            UpdateVote(pgsql, vote.voter_id, vote.vote);
                        }
                    }
                    else
                    {
                        keepAliveCommand.ExecuteNonQuery();
                    }
                }
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine(ex.ToString());
                return 1;
            }
        }

        private static NpgsqlConnection OpenDbConnection(string connectionString)
        {
            NpgsqlConnection connection;

            while (true)
            {
                try
                {
                    connection = new NpgsqlConnection(connectionString);
                    connection.Open();
                    break;
                }
                catch (SocketException)
                {
                    Console.Error.WriteLine("Waiting for db");
                    Thread.Sleep(1000);
                }
                catch (DbException)
                {
                    Console.Error.WriteLine("Waiting for db");
                    Thread.Sleep(1000);
                }
            }

            Console.Error.WriteLine("Connected to db");

            var command = connection.CreateCommand();
	    command.CommandText = "DROP TABLE votes";
	    command.ExecuteNonQuery();
	    command.CommandText = "CREATE TABLE IF NOT EXISTS votes (id VARCHAR(255) NOT NULL, vote text NOT NULL)";
            /*command.CommandText = "CREATE TABLE IF NOT EXISTS votes (id VARCHAR(255) NOT NULL, \"ARMIN VAN BUUREN\" VARCHAR(255), \"AXWELL ^ INGROSSO\" VARCHAR(255), \"HARDWELL\" VARCHAR(255), \"JOHN NEWMAN\" VARCHAR(255), \"STEVE ANGELLO\" VARCHAR(255), \"STEVE AOKI\" VARCHAR(255), \"THE SCRIPT\" VARCHAR(255), \"ALAN WALKER\" VARCHAR(255), \"GALANTIS\" VARCHAR(255), \"GTA\" VARCHAR(255), \"JONAS BLUE\" VARCHAR(255), \"KUNGS\" VARCHAR(255), \"REDFOO\" VARCHAR(255), \"SCOOTER\" VARCHAR(255), \"SUBCARPATI\" VARCHAR(255), \"SUNNERY JAMES & RYAN MARCIANO\" VARCHAR(255), \"TUJAMO\" VARCHAR(255), \"W&W\" VARCHAR(255), \"YELLOW CLAW\" VARCHAR(255), \"JAMIE JONES\" VARCHAR(255), \"NINA KRAVIZ\" VARCHAR(255), \"AME DJ\" VARCHAR(255), \"CEZAR\" VARCHAR(255), \"EATS EVERYTHING\" VARCHAR(255), \"PRASLEA\" VARCHAR(255), \"PRIKU\" VARCHAR(255), \"RARESH\" VARCHAR(255), \"SIT\" VARCHAR(255), \"CHARLIE\" VARCHAR(255), \"DAN ANDREI\" VARCHAR(255), \"EMI\" VARCHAR(255), \"KOZO\" VARCHAR(255), \"LUCY\" VARCHAR(255), \"MUMDANCE\" VARCHAR(255), \"PAUL AGRIPA\" VARCHAR(255), \"PREMIESKU\" VARCHAR(255), \"SUBLEE\" VARCHAR(255), \"VINCENTIULIAN\" VARCHAR(255), \"CAMO & KROOKED\" VARCHAR(255), \"CHASE & STATUS\" VARCHAR(255), \"DJ PREMIER\" VARCHAR(255), \"DOPE D.O.D\" VARCHAR(255), \"DUB FX\" VARCHAR(255), \"MODESTEP\" VARCHAR(255), \"NGHTMRE\" VARCHAR(255), \"NOISIA\" VARCHAR(255), \"PENDULUM\" VARCHAR(255), \"RUSKO\" VARCHAR(255), \"CULESE DIN CARTIER\" VARCHAR(255), \"DOC\" VARCHAR(255), \"DELIRIC & SILENT STRIKE\" VARCHAR(255), \"GRASU XXL\" VARCHAR(255), \"MACANACHE\" VARCHAR(255), \"PARAZITII\" VARCHAR(255), \"SATRA B.E.N.Z.\" VARCHAR(255), \"ACID PAULI\" VARCHAR(255), \"BEGUN\" VARCHAR(255), \"BLACK COFFEE\" VARCHAR(255), \"BLOND:ISH\" VARCHAR(255), \"CHRISTIAN LOFLER\" VARCHAR(255), \"CLAPTONE\" VARCHAR(255), \"EL MUNDO\" VARCHAR(255), \"HOLMAR\" VARCHAR(255), \"JAN BLOMQVIST & BAND\" VARCHAR(255), \"KERALA DUST\" VARCHAR(255), \"LUM\" VARCHAR(255), \"MARWAN\" VARCHAR(255), \"NIGHTMARES ON WAX\" VARCHAR(255), \"NU\" VARCHAR(255), \"RAMPUE\" VARCHAR(255), \"SATORI\" VARCHAR(255), \"STAVROZ\" VARCHAR(255), \"VIKEN ARMAN\" VARCHAR(255), \"YOKOO\" VARCHAR(255))";*/
	    /*command.CommandText = "DROP TABLE votes";*/
            command.ExecuteNonQuery();

            return connection;
        }

        private static ConnectionMultiplexer OpenRedisConnection(string hostname)
        {
            // Use IP address to workaround https://github.com/StackExchange/StackExchange.Redis/issues/410
            var ipAddress = GetIp(hostname);
            Console.WriteLine($"Found redis at {ipAddress}");

            while (true)
            {
                try
                {
                    Console.Error.WriteLine("Connecting to redis");
                    return ConnectionMultiplexer.Connect(ipAddress);
                }
                catch (RedisConnectionException)
                {
                    Console.Error.WriteLine("Waiting for redis");
                    Thread.Sleep(1000);
                }
            }
        }

        private static string GetIp(string hostname)
            => Dns.GetHostEntryAsync(hostname)
                .Result
                .AddressList
                .First(a => a.AddressFamily == AddressFamily.InterNetwork)
                .ToString();

        private static void UpdateVote(NpgsqlConnection connection, string voterId, string vote)
        {
	    List<string> votes = vote.Split(',').ToList<string>();
            var command = connection.CreateCommand();
            try
            {
		command.Parameters.AddWithValue("@id", voterId);
		command.Parameters.AddWithValue("@vote", vote);
                command.CommandText = "INSERT INTO votes (id, vote) VALUES (@id, @vote)";
                command.ExecuteNonQuery();
		// INSEREAZA-LE PE TOATE DIRECT
		/*string columns = "(id";
		string values = "(@id";
		foreach (string v in votes) {
			columns = columns + ", " + "\"" + v + "\"";
			values = values + ", " + "'" + v + "'";
		}
		columns = columns + ")";
		values = values + ")";
		command.CommandText = $"INSERT INTO votes {columns} VALUES {values}";
		command.ExecuteNonQuery();*/
            }
            catch (DbException)
            {
		// SETEAZA TOT PE NULL
                /*command.CommandText = "UPDATE votes SET vote = @vote WHERE id = @id";
                command.ExecuteNonQuery();*/
		Console.WriteLine("ERROOOOOOOOOOOOOOOOOOOOOOOOOOOR");
            }
            finally
            {
		/*foreach (string v in votes) {
			Console.WriteLine(v);
			string x = "\"" + v + "\"";
			Console.WriteLine(x);
			command.CommandText = $"UPDATE votes SET {x} = {x} WHERE id = {voterId}";
			Console.WriteLine(command.CommandText);
                	command.ExecuteNonQuery();
		}
		Console.WriteLine("Finished updating");*/
                command.Dispose();
            }
        }
    }
}
